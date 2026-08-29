import torch
import torch.nn as nn
import torchvision as vs
import torch.utils.data as utils
from tqdm import tqdm
import torch.nn.functional as F
import bitsandbytes as bnb
from transformers import CLIPTokenizer, CLIPTextModel


class Diffusion(nn.Module):
    def __init__(self):
        super().__init__()
        betas = torch.linspace(1e-4, 0.02, 1000)
        alphas = 1.0 - betas
        alpha_hats = torch.cumprod(alphas, dim=0)
        one_minus = torch.sqrt(1.0 - alpha_hats)
        sqrt_alpha_hats = torch.sqrt(alpha_hats)

        self.register_buffer("betas", betas)
        self.register_buffer("alphas", alphas)
        self.register_buffer("alpha_hats", alpha_hats)
        self.register_buffer("one_minus", one_minus)
        self.register_buffer("sqrt_alpha_hats", sqrt_alpha_hats)

    def forward(self, x, t):
        noise = torch.randn_like(x, device=x.device)
        xt = (self.sqrt_alpha_hats[t][:, None, None, None] * x +
              self.one_minus[t][:, None, None, None] * noise)
        return xt, noise


class CrossAttention(nn.Module):
    def __init__(self, in_c, ctx_dim, heads=8):
        super().__init__()
        assert in_c % heads == 0
        self.heads = heads
        self.dim = in_c // heads
        self.norm = nn.GroupNorm(min(32, in_c), in_c)
        self.q = nn.Conv2d(in_c, in_c, 1, bias=False)
        self.k = nn.Linear(ctx_dim, in_c, bias=False)
        self.v = nn.Linear(ctx_dim, in_c, bias=False)
        self.proj = nn.Conv2d(in_c, in_c, 1)

    def forward(self, x, context):
        B, C, H, W = x.shape

        h = self.norm(x)
        q = self.q(h)
        q = q.flatten(2).transpose(1, 2)
        q = q.view(B, H * W, self.heads, self.dim).transpose(1, 2)

        k = self.k(context)
        v = self.v(context)
        k = k.view(B, -1, self.heads, self.dim).transpose(1, 2)
        v = v.view(B, -1, self.heads, self.dim).transpose(1, 2)

        out = F.scaled_dot_product_attention(q, k, v)

        out = out.transpose(1, 2).contiguous().reshape(B, H * W, C)
        out = out.transpose(1, 2).reshape(B, C, H, W)
        return self.proj(out)


class TimeEmb(nn.Module):
    def __init__(self, dim):
        super().__init__()
        assert dim % 2 == 0
        self.dim = dim
        half = self.dim // 2
        te = torch.exp(-torch.log(torch.tensor(10000.0)) / half * torch.arange(half))
        self.register_buffer("te", te)

    def forward(self, t):
        device = t.device
        te = t[:, None].float() * self.te[None, :]
        res = torch.zeros(t.size(0), self.dim, device=device)
        res[:, 0::2] = te.sin()
        res[:, 1::2] = te.cos()
        return res


class Residual(nn.Module):
    def __init__(self, in_c, out_c, tdim=128):
        super().__init__()
        self.TE = TimeEmb(tdim)
        self.time = nn.Linear(tdim, out_c)

        self.id = nn.Conv2d(in_c, out_c, 1, bias=False) if in_c != out_c else nn.Identity()

        self.conv1 = nn.Conv2d(in_c, out_c, 3, padding=1)
        groups = 8 if out_c % 8 == 0 else 1
        self.gn1 = nn.GroupNorm(groups, out_c)
        self.drop1 = nn.Dropout2d(0.1)

        self.conv2 = nn.Conv2d(out_c, out_c, 3, padding=1)
        self.gn2 = nn.GroupNorm(groups, out_c)

    def forward(self, x, t):
        identity = self.id(x)

        x = torch.relu(self.gn1(self.conv1(x)))
        x = self.drop1(x)

        x = self.gn2(self.conv2(x))

        condition = self.TE(t)
        condition = self.time(condition)[:, :, None, None]

        x = x + condition
        x = x + identity

        return torch.relu(x)


class Unet(nn.Module):
    def __init__(self, in_c=1, feat=64, out_c=1, tdim=128, ctx_dim=512):
        super().__init__()
        self.pool = nn.MaxPool2d(2)

        self.d1 = Residual(in_c, feat, tdim)
        self.d2 = Residual(feat, feat * 2, tdim)
        self.d3 = Residual(feat * 2, feat * 4, tdim)
        self.mh1 = CrossAttention(feat * 4, ctx_dim)

        self.bottle = Residual(feat * 4, feat * 8, tdim)
        self.mh2 = CrossAttention(feat * 8, ctx_dim)

        self.up1 = nn.ConvTranspose2d(feat * 8, feat * 4, 2, 2)
        self.res1 = Residual(feat * 8, feat * 4, tdim)
        self.mh3 = CrossAttention(feat * 4, ctx_dim)

        self.up2 = nn.ConvTranspose2d(feat * 4, feat * 2, 2, 2)
        self.res2 = Residual(feat * 4, feat * 2, tdim)

        self.up3 = nn.ConvTranspose2d(feat * 2, feat, 2, 2)
        self.res3 = Residual(feat * 2, feat, tdim)

        self.final = nn.Conv2d(feat, out_c, 1)

    def forward(self, x, t, context):
        d1 = self.d1(x, t)
        d2 = self.d2(self.pool(d1), t)
        d3 = self.d3(self.pool(d2), t)
        d3 = self.mh1(d3, context) + d3

        x = self.bottle(self.pool(d3), t)
        x = self.mh2(x, context) + x

        x = self.res1(torch.cat([self.up1(x), d3], dim=1), t)
        x = self.mh3(x, context) + x
        x = self.res2(torch.cat([self.up2(x), d2], dim=1), t)
        x = self.res3(torch.cat([self.up3(x), d1], dim=1), t)
        x = self.final(x)
        return x


class TextEncoder(nn.Module):
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        super().__init__()
        self.tokenizer = CLIPTokenizer.from_pretrained(model_name)
        self.model = CLIPTextModel.from_pretrained(model_name)
        self.model.eval()
        for p in self.model.parameters():
            p.requires_grad = False

    @torch.no_grad()
    def forward(self, prompts, device):
        tokens = self.tokenizer(
            prompts, padding=True, truncation=True, return_tensors="pt"
        ).to(device)
        out = self.model(**tokens)
        return out.last_hidden_state


device = "cuda" if torch.cuda.is_available() else "cpu"

DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class MNISTCaptioned(utils.Dataset):
    def __init__(self, mnist_dataset):
        self.data = mnist_dataset

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img, label = self.data[idx]
        prompt = f"the digit {DIGIT_WORDS[label]}"
        return img, prompt


def train():
    torch.backends.cudnn.benchmark = True
    torch.set_float32_matmul_precision("high")

    text_encoder = TextEncoder().to(device)
    model = Unet(ctx_dim=512).to(device)
    diff = Diffusion().to(device)

    tr = vs.transforms
    trans = tr.Compose([tr.ToTensor(), tr.Normalize((0.5,), (0.5,)), tr.Resize(64)])
    raw_data = vs.datasets.MNIST("data", train=True, transform=trans, download=True)
    data = MNISTCaptioned(raw_data)
    loader = utils.DataLoader(data, batch_size=32, shuffle=True,
                               num_workers=4, persistent_workers=True)

    optimizer = bnb.optim.AdamW8bit(model.parameters(), lr=8e-05, weight_decay=1e-4)
    criterion = nn.MSELoss()
    scaler = torch.amp.GradScaler("cuda")

    epochs = 20
    data_len = len(loader)
    warmup_steps = data_len
    total_steps = epochs * data_len
    warmup = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=1e-5, total_iters=warmup_steps)
    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=total_steps - warmup_steps, eta_min=1e-6)
    scheduler = torch.optim.lr_scheduler.SequentialLR(optimizer, schedulers=[warmup, cosine], milestones=[warmup_steps])

    losses = []

    for epoch in range(epochs):
        model.train()
        ep_loss = 0

        progress = tqdm(loader, desc=f"epoch {epoch+1}/{epochs}")

        for batch, prompts in progress:
            batch = batch.to(device)
            context = text_encoder(list(prompts), device=device)

            optimizer.zero_grad()
            t = torch.randint(0, 1000, (batch.size(0),)).to(device)
            dbatch, z = diff(batch, t)

            with torch.amp.autocast("cuda", enabled=True):
                preds = model(dbatch, t, context)
                loss = criterion(preds, z)

            ep_loss += loss.item()

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            progress.set_postfix(loss=f"{loss.item():.6f}", lr=f"{scheduler.get_last_lr()[0]:.2e}")

        losses.append(ep_loss / data_len)
        torch.save({
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "scaler": scaler.state_dict(),
            "losses": losses,
            "epoch": epoch,
        }, "dmodel_t2i_v1.pt")


if __name__ == '__main__':
    train()
