import joblib
import pandas as pd
import torch
import torch.nn as nn

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from torch.optim import Adam
from torch.utils.data import TensorDataset, DataLoader


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
# Load Dataset
# =====================================

df = pd.read_csv("clean_data.csv")

target = pd.read_csv("ai_student_impact_dataset.csv")[
    "Post_Semester_GPA"
].astype("float32")

X_train_df, X_test_df, y_train, y_test = train_test_split(
    df,
    target,
    test_size=0.20,
    random_state=42
)


# =====================================
# Preprocessing
# =====================================

categorical_cols = [
    "Major_Category",
    "Primary_Use_Case",
    "Prompt_Engineering_Skill",
    "Paid_Subscription"
]

numerical_cols = [
    col for col in X_train_df.columns
    if col not in categorical_cols
]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer()),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("encoder", OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    ))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numerical_cols),
    ("cat", categorical_pipeline, categorical_cols)
])

X_train = preprocessor.fit_transform(X_train_df)
X_test = preprocessor.transform(X_test_df)

joblib.dump(preprocessor, "preprocessing.pkl")


# =====================================
# Torch Tensors
# =====================================

X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
X_test = torch.tensor(X_test, dtype=torch.float32).to(device)

y_train = torch.tensor(
    y_train.values,
    dtype=torch.float32
).view(-1, 1).to(device)

y_test = torch.tensor(
    y_test.values,
    dtype=torch.float32
).view(-1, 1).to(device)


# =====================================
# DataLoaders
# =====================================

train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    TensorDataset(X_test, y_test),
    batch_size=32,
    shuffle=False
)


# =====================================
# Model
# =====================================

model = SimpleANN(X_train.shape[1]).to(device)

optimizer = Adam(
    model.parameters(),
    lr=1e-4,
    weight_decay=1e-4
)

criterion = nn.MSELoss()


# =====================================
# Training
# =====================================

epochs = 150

for epoch in range(epochs):

    model.train()

    train_loss = 0

    for X_batch, y_batch in train_loader:

        optimizer.zero_grad()

        prediction = model(X_batch)

        loss = criterion(prediction, y_batch)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

    print(
        f"Epoch {epoch + 1:3d} | "
        f"Train Loss: {train_loss / len(train_loader):.4f}"
    )


# =====================================
# Save Model
# =====================================

torch.save(model.state_dict(), "model.pth")

print("\nModel saved.")


# =====================================
# Evaluation
# =====================================

model.eval()

test_loss = 0

with torch.no_grad():

    for X_batch, y_batch in test_loader:

        prediction = model(X_batch)

        test_loss += criterion(
            prediction,
            y_batch
        ).item()

print(f"Test Loss: {test_loss / len(test_loader):.4f}")
