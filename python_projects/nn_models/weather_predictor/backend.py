import os
import numpy as np
import matplotlib.pyplot as plt
import torch

from minT_graph import convLSTMFPN as TempModel
from minT_graph import MinTempData
from rainfall_graph import convLSTMFPN as RainModel
from rainfall_graph import MinTempData2

OUTPUT_FOLDER = r"D:\web\project-04\src\assets"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

temp_model = TempModel(3, 192, 1).to(device)
temp_model.load_state_dict(
    torch.load("best_minT_model.pt", map_location=device)
)
temp_model.eval()

rain_model = RainModel(3, 192, 1).to(device)
rain_model.load_state_dict(
    torch.load("best_rain_model.pt", map_location=device)
)
rain_model.eval()


def save_heatmap(prediction, actual, filename):

    if np.any(actual == -999):
        mask = actual == -999
        cmap = plt.cm.Blues.copy()
    else:
        mask = actual == 99.9
        cmap = plt.cm.coolwarm.copy()

    prediction = np.ma.masked_where(mask, prediction)

    cmap.set_bad(alpha=0)

    plt.figure(figsize=(5, 5))

    plt.imshow(
        prediction,
        origin="lower",
        cmap=cmap
    )

    plt.axis("off")

    plt.savefig(
        os.path.join(OUTPUT_FOLDER, filename),
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True
    )

    plt.close()

def predict_temperature():

    os.makedirs(os.path.join(OUTPUT_FOLDER, "temperature"), exist_ok=True)

    files = [
        "Mintemp_MinT_2020.grd",
        "Mintemp_MinT_2021.grd",
        "Mintemp_MinT_2022.grd",
        "Mintemp_MinT_2023.grd",
        "Mintemp_MinT_2024.grd",
        "Mintemp_MinT_2025.grd",
    ]

    arrays = []

    for f in files:
        arr = np.fromfile(f, dtype=np.float32)
        arrays.append(arr.reshape(-1, 31, 31))

    lengths = [a.shape[0] for a in arrays]

    data = np.concatenate(arrays, axis=0)

    doy = np.concatenate(
        [np.arange(l) for l in lengths]
    ).astype(np.float32)

    sin_doy = np.sin(
        2 * np.pi * doy / 365.25
    )

    cos_doy = np.cos(
        2 * np.pi * doy / 365.25
    )

    dataset = MinTempData(
        data,
        sin_doy,
        cos_doy,
        window=30
    )

    NUM_FRAMES = 200

    start = len(dataset) - NUM_FRAMES

    for i, idx in enumerate(range(start, len(dataset)), start=1):

        x, _, _ = dataset[idx]

        x = x.unsqueeze(0).to(device)

        with torch.no_grad():
            pred = temp_model(x)

        pred = pred.squeeze().cpu().numpy()

        pred = pred[:31, :31]

        pred = pred * dataset.std + dataset.mean

        actual = data[idx + dataset.window]

        save_heatmap(
            pred,
            actual,
            os.path.join(
                "temperature",
                f"temperature_{i:03d}.png"
            )
        )

    print("Temperature frames written")


def predict_rainfall():

    os.makedirs(os.path.join(OUTPUT_FOLDER, "rainfall"), exist_ok=True)

    files = [
        "Rainfall_ind2022_rfp25.grd",
        "Rainfall_ind2023_rfp25.grd",
        "Rainfall_ind2024_rfp25.grd",
        "Rainfall_ind2025_rfp25.grd",
    ]

    arrays = [
        np.fromfile(f, dtype=np.float32).reshape(-1, 129, 135)
        for f in files
    ]

    lengths = [a.shape[0] for a in arrays]

    data = np.concatenate(arrays, axis=0)

    doy = np.concatenate(
        [np.arange(l) for l in lengths]
    ).astype(np.float32)

    sin_doy = np.sin(
        2 * np.pi * doy / 365.25
    )

    cos_doy = np.cos(
        2 * np.pi * doy / 365.25
    )

    dataset = MinTempData2(
        data,
        sin_doy,
        cos_doy,
        window=7
    )

    NUM_FRAMES = 200

    start = len(dataset) - NUM_FRAMES

    for i, idx in enumerate(range(start, len(dataset)), start=1):

        x, _, _ = dataset[idx]

        x = x.unsqueeze(0).to(device)

        with torch.no_grad():
            pred = rain_model(x)

        pred = pred.squeeze().cpu().numpy()

        pred = pred[3:132, 0:135]

        pred = pred * (
            dataset.orig_max - dataset.orig_min
        ) + dataset.orig_min

        pred = np.expm1(pred)

        actual = data[idx + dataset.window]

        save_heatmap(
            pred,
            actual,
            os.path.join(
                "rainfall",
                f"rainfall_{i:03d}.png"
            )
        )

    print("Rainfall frames written")


if __name__ == "__main__":

    predict_temperature()

    predict_rainfall()

    print("Finished.")
