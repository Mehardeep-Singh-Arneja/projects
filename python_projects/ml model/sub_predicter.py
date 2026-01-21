import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

MODEL_FILE = "model.pkl"
PIPELINE_FILE = "pipeline.pkl"

test = pd.read_csv("test/test.csv")
features = pd.read_csv("train/features.csv")
labels = pd.read_csv("train/labels.csv")

cat_cols = [
    "income_level",
    "preferred_content_theme",
    "privacy_setting_level",
    "two_factor_auth_enabled"
]

num_cols = [c for c in features.columns if c not in cat_cols]

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pipeline = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_cols),
    ("cat", cat_pipeline, cat_cols)
])

X_train = full_pipeline.fit_transform(features)
y_train = labels.iloc[:, 0]

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    class_weight={
        "Free": 1,
        "Premium": 4,
        "Business": 4
    },
    min_samples_leaf=5
)
print("now training.....")
model.fit(X_train, y_train)

X_test = full_pipeline.transform(test)
predictions = model.predict(X_test)

print(predictions[:10])
joblib.dump(model, MODEL_FILE)
joblib.dump(full_pipeline, PIPELINE_FILE)
