import torch
import torch.nn as nn
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split


# =====================================
# Model
# =====================================

class SimpleANN(nn.Module):
    def __init__(self, input_features):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_features, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(32, 10),
            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(10, 1)
        )

    def forward(self, x):
        return self.network(x)


# =====================================
# Device
# =====================================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# =====================================
# Load Preprocessor
# =====================================

preprocessor = joblib.load("preprocessing.pkl")


# =====================================
# Load Test Data
# =====================================

X = pd.read_csv("clean_data.csv")

y = pd.read_csv("ai_student_impact_dataset.csv")[
    "Post_Semester_GPA"
].astype("float32")

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)


# =====================================
# Preprocess
# =====================================

X_test = preprocessor.transform(X_test)

input_features = X_test.shape[1]

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
).to(device)


# =====================================
# Load Model
# =====================================

model = SimpleANN(input_features)

model.load_state_dict(
    torch.load("model.pth", map_location=device)
)

model.to(device)
model.eval()


# =====================================
# Predict
# =====================================

with torch.no_grad():
    predictions = model(X_test)

predictions = predictions.cpu().numpy().flatten()


# =====================================
# Results
# =====================================

# print("\nPrediction Results\n")

# for pred, actual in zip(predictions, y_test):
#     print(f"Predicted: {pred:.2f} | Actual: {actual:.2f}")
tolerance = 0.5

accuracy = np.mean(
    np.abs(predictions - y_test.to_numpy()) <= tolerance
)

print(f"Accuracy (±{tolerance} GPA): {accuracy*100:.2f}%")
