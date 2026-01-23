import joblib
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from tensorflow.python.data.ops.dataset_ops import ShuffleDataset

df = pd.read_csv("tictactoe.csv")
df = df.sample(frac=1,random_state=42)
# df.drop_duplicates(inplace=True)

X = df.iloc[:, :-1]
y = df["decision"]

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("model", ExtraTreesClassifier(
        n_estimators=300,
        random_state=42
    ))
])

pipeline.fit(X, y)

joblib.dump(pipeline, "model.pkl")
