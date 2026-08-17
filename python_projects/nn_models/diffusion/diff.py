import torch
import torch.nn as nn
import torchvision as vs
import torch.utils.data as utils
from tqdm import tqdm

class Diffusion(nn.Module):
    def __init__(self):
        super().__init__()
        betas = torch.linspace(1e-4,0.02,1000) # 1000
        alphas = 1.0 - betas
        alpha_hats = torch.cumprod(alphas, dim=0)
        one_minus = torch.sqrt(1.0 - alpha_hats)
        sqrt_alpha_hats = torch.sqrt(alpha_hats)

        self.register_buffer("betas",betas)
        self.register_buffer("alphas", alphas)
        self.register_buffer("alpha_hats", alpha_hats)
        self.register_buffer("one_minus", one_minus)
        self.register_buffer("sqrt_alpha_hats", sqrt_alpha_hats)

    def forward(self,x,t): # t -> 32
        noise = torch.randn_like(x,device=x.device) # 32x1x64x64
        xt = (self.sqrt_alpha_hats[t][:,None,None,None]*x +
              self.one_minus[t][:,None,None,None]*noise)
        return xt,noise

class Mha(nn.Module):
    def __init__(self, in_c, heads=8):
        super().__init__()
        assert in_c % heads == 0, f"in_c={in_c} not divisible by heads={heads}"
        self.heads = heads
        self.dim = in_c // heads
        self.norm = nn.GroupNorm(min(32, in_c), in_c)
        self.q = nn.Conv2d(in_c, in_c, 1, bias=False)
        self.k = nn.Conv2d(in_c, in_c, 1, bias=False)
        self.v = nn.Conv2d(in_c, in_c, 1, bias=False)
        self.proj = nn.Conv2d(in_c, in_c, 1)

    def forward(self, x):
        B, C, H, W = x.shape
        h = self.norm(x)
        q = self.q(h)
        k = self.k(h)
        v = self.v(h)
        q = q.flatten(2).transpose(1, 2).view(B, H * W, self.heads, self.dim).transpose(1, 2)
        k = k.flatten(2).transpose(1, 2).view(B, H * W, self.heads, self.dim).transpose(1, 2)
        v = v.flatten(2).transpose(1, 2).view(B, H * W, self.heads, self.dim).transpose(1, 2)
        scores = q @ k.transpose(-2, -1) / (self.dim ** 0.5)
        W_attn = torch.softmax(scores, dim=-1)
        out = W_attn @ v
        out = out.transpose(1, 2).contiguous().view(B, H * W, C)
        out = out.transpose(1, 2).reshape(B, C, H, W)
        return self.proj(out)

class Residual(nn.Module):
    def __init__(self,in_c,out_c,tdim=128):
        super().__init__()
        self.TE=TimeEmb(tdim)
        self.CE=nn.Embedding(10,tdim)
        self.time=nn.Linear(tdim,out_c)

        self.id=nn.Conv2d(in_c,out_c,1,bias=False) if in_c!=out_c else nn.Identity()

        self.conv1=nn.Conv2d(in_c,out_c,3,padding=1)
        groups=8 if out_c%8==0 else 1
        self.gn1=nn.GroupNorm(groups,out_c)
        self.drop1=nn.Dropout2d(0.1)

        self.conv2=nn.Conv2d(out_c,out_c,3,padding=1)
        self.gn2=nn.GroupNorm(groups,out_c)

    def forward(self,x,t,y):
        identity=self.id(x)

        x=torch.relu(self.gn1(self.conv1(x)))
        x=self.drop1(x)

        x=self.gn2(self.conv2(x))

        condition=self.TE(t)+self.CE(y)
        condition=self.time(condition)[:,:,None,None]

        x=x+condition
        x=x+identity

        return torch.relu(x)

class TimeEmb(nn.Module):
    def __init__(self, dim):
        super().__init__()
        assert dim % 2 == 0, "TimeEmb dim must be even"
        self.dim = dim
        half = self.dim // 2
        te = torch.exp(-torch.log(torch.tensor(10000.0)) / half * torch.arange(half))
        self.register_buffer("te",te)

    def forward(self, t):
        device = t.device
        te = t[:, None].float() * self.te[None, :]
        res = torch.zeros(t.size(0), self.dim, device=device)
        res[:, 0::2] = te.sin()
        res[:, 1::2] = te.cos()
        return res

class Unet(nn.Module):
    def __init__(self,in_c=1,feat=64,out_c=1,tdim=128):
        super().__init__()
        self.pool = nn.MaxPool2d(2)

        self.d1 = Residual(in_c, feat,tdim)
        self.d2 = Residual(feat, feat*2,tdim)
        self.d3 = Residual(feat*2, feat * 4,tdim)
        self.mh1 = Mha(feat * 4)

        self.bottle = Residual(feat*4, feat * 8,tdim)
        self.mh2 = Mha(feat * 8)

        self.up1 = nn.ConvTranspose2d(feat*8,feat*4,2,2)
        self.res1 = Residual(feat*8,feat*4,tdim)
        self.mh3 = Mha(feat*4)

        self.up2 = nn.ConvTranspose2d(feat * 4, feat * 2, 2, 2)
        self.res2 = Residual(feat * 4, feat * 2, tdim)

        self.up3 = nn.ConvTranspose2d(feat * 2, feat, 2, 2)
        self.res3 = Residual(feat * 2, feat, tdim)

        self.final = nn.Conv2d(feat,out_c,1)

    def forward(self,x,t,y):
        d1 = self.d1(x,t,y)
        d2 = self.d2(self.pool(d1),t,y)
        d3 = self.d3(self.pool(d2),t,y)
        d3 = self.mh1(d3)+d3

        x = self.bottle(self.pool(d3),t,y)
        x = self.mh2(x)+x

        x = self.res1(torch.cat([self.up1(x),d3],dim=1),t,y)
        x = self.mh3(x)+x
        x = self.res2(torch.cat([self.up2(x), d2], dim=1), t,y)
        x = self.res3(torch.cat([self.up3(x), d1], dim=1), t,y)
        x = self.final(x)
        return x

def train():
    model = Unet().cuda()
    diff = Diffusion().cuda()
    tr = vs.transforms
    trans = tr.Compose([tr.ToTensor(), tr.Normalize((0.5,), (0.5,)), tr.Resize(64)])
    data = vs.datasets.MNIST("data", train=True, transform=trans, download=True)
    loader = utils.DataLoader(data, 32, True,
                              num_workers=4, persistent_workers=True)
    optimizer = torch.optim.AdamW(model.parameters(),lr=1e-4,weight_decay=1e-4)

    criterion = nn.MSELoss()
    scaler = torch.amp.GradScaler("cuda")
    losses = []
    epochs = 20
    data_len = len(loader)
    warmup_steps = data_len
    total_steps = epochs * data_len
    warmup = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=1e-3, total_iters=warmup_steps)
    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=total_steps - warmup_steps, eta_min=1e-6)
    scheduler = torch.optim.lr_scheduler.SequentialLR(optimizer, schedulers=[warmup, cosine], milestones=[warmup_steps])
    for epoch in range(epochs):
        model.train()
        ep_loss = 0

        progress = tqdm(loader,desc=f"epoch {epoch+1}/{epochs}")

        for batch, y in progress:
            batch,y = batch.cuda(),y.cuda()
            optimizer.zero_grad()
            t = torch.randint(0, 1000, (batch.size(0),)).cuda()
            dbatch, z = diff(batch, t)
            with torch.amp.autocast("cuda"):
                preds = model(dbatch,t,y)
                loss = criterion(preds,z)
            ep_loss += loss.item()

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            progress.set_postfix(loss=f"{loss.item():.6f}", lr=f"{scheduler.get_last_lr()[0]:.2e}")
        losses.append(ep_loss/data_len)
        torch.save({
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "losses": losses,
            "epoch": epoch,
        }, "dmodel_v1.pt")

if __name__ == '__main__':
    train()
