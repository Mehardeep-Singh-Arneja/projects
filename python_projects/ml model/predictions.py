import joblib
import pandas as pd
import numpy as np
import sklearn.pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

input = pd.read_csv("test/test.csv")
input.drop("subscription_status",axis=1,inplace=True)
trans = pipeline.transform(input)

preds = model.predict(trans)
output = pd.DataFrame(preds)
output.to_csv("output.csv")

