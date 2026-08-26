import matplotlib.pyplot as plt
from tqdm import tqdm
from diff_practice import Unet, Diffusion
import torch
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def loss_plot():
    checkpoint = torch.load("dmodel_v1.pt", map_location="cuda")
    model = Unet().cuda()
    model.load_state_dict(checkpoint["model"])

    plt.plot(checkpoint["losses"])
    plt.show()

@torch.no_grad()
def reverse(diff, model, x, t, y):
    eps = model(x, t, y)

    alpha = diff.alphas[t][:, None, None, None]
    alpha_hat = diff.alpha_hats[t][:, None, None, None]
    beta = diff.betas[t][:, None, None, None]

    mean = (1 / torch.sqrt(alpha)) * (x - (beta / torch.sqrt(1 - alpha_hat)) * eps)

    if t[0] == 0:
        return mean

    noise = torch.randn_like(x)
    return mean + torch.sqrt(beta) * noise

@torch.no_grad()
def sample(model, diff, y, n=16):
    model.eval()

    x = torch.randn(
        n, 1, 64, 64,
        device=next(model.parameters()).device
    )

    progress = tqdm(reversed(range(1000)), total=1000, desc="generating your image ;) ")
    for i in progress:
        t = torch.full(
            (n,),
            i,
            device=x.device,
            dtype=torch.long
        )

        x = reverse(diff, model, x, t, y)

    return x

device = "cuda" if torch.cuda.is_available() else "cpu"

checkpoint = torch.load(
    "dmodel_v1.pt",
    map_location=device
)

model = Unet().to(device)
model.load_state_dict(checkpoint["model"])
model.eval()
diff = Diffusion().to(device)

@app.route("/diffusion",methods = ["POST"])
def sample_images():
    digit = request.get_json()["number"]

    n = 5
    if digit is None:
        y = torch.randint(0, 10, (n,), device=device)
    else:
        y = torch.full((n,), digit, device=device, dtype=torch.long)

    images = sample(model, diff, y, n)

    images = images.clamp(-1, 1)
    images = (images + 1) / 2

    fig, axes = plt.subplots(1, 5, figsize=(6, 2))
    for ax, img, label in zip(axes.flat, images, y.cpu()):
        ax.imshow(img[0].cpu(), cmap="gray")
        ax.set_title("")
        ax.axis("off")

    plt.savefig("gen_img.png")
    return jsonify({
        "digit":digit,
        "image":"/gentd"
    })

@app.route("/gentd",methods = ["GET"])
def gen_img():
    return send_file("gen_img.png")

if __name__ == '__main__':
    app.run("0.0.0.0",5000)
