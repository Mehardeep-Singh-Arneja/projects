import torch
import matplotlib.pyplot as plt
from tqdm import tqdm

from diff import Unet, Diffusion, TextEncoder


device = "cuda" if torch.cuda.is_available() else "cpu"


@torch.no_grad()
def reverse(diff, model, x, t, context):
    eps = model(x, t, context)

    alpha = diff.alphas[t][:, None, None, None]
    alpha_hat = diff.alpha_hats[t][:, None, None, None]
    beta = diff.betas[t][:, None, None, None]

    mean = (1 / torch.sqrt(alpha)) * (
        x - (beta / torch.sqrt(1 - alpha_hat)) * eps
    )

    if t[0] == 0:
        return mean

    noise = torch.randn_like(x)
    return mean + torch.sqrt(beta) * noise


@torch.no_grad()
def sample(model, diff, text_encoder, prompts, n=None):
    model.eval()

    if n is None:
        n = len(prompts)

    context = text_encoder(prompts, device=device)

    x = torch.randn(n, 1, 64, 64, device=device)

    progress = tqdm(reversed(range(1000)), total=1000, desc="generating")
    for i in progress:
        t = torch.full((n,), i, device=device, dtype=torch.long)
        x = reverse(diff, model, x, t, context)

    return x


def sample_images(prompts, checkpoint_path="dmodel_t2i_v1.pt"):
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model = Unet(ctx_dim=512).to(device)
    model.load_state_dict(checkpoint["model"])
    model.eval()

    diff = Diffusion().to(device)
    text_encoder = TextEncoder().to(device)

    images = sample(model, diff, text_encoder, prompts)

    images = images.clamp(-1, 1)
    images = (images + 1) / 2

    n = len(prompts)
    fig, axes = plt.subplots(1, n, figsize=(3 * n, 3))
    if n == 1:
        axes = [axes]

    for ax, img, prompt in zip(axes, images, prompts):
        ax.imshow(img[0].cpu(), cmap="gray")
        ax.set_title(prompt, fontsize=10)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("gen_t2i.png")
    plt.show()


if __name__ == "__main__":
    prompts = [
        "the digit three five",
        "the digit three five",
        "the digit three five",
        "the digit three five",
    ]
    sample_images(prompts)
