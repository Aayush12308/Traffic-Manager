import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import QuantileTransformer



def normalisedf(df):
    scaler = QuantileTransformer(output_distribution='normal')
    df[['CarCount', 'BikeCount', 'BusCount', 'TruckCount']] = scaler.fit_transform(df[['CarCount', 'BikeCount', 'BusCount', 'TruckCount']])
    print(df)
    return df



def load_model():
    pipeline = joblib.load("/Users/akashzamnani/Desktop/Traffic-BE-proj/Traffic-Manager/model/traffic_pipeline1.pkl",)
    return pipeline

def run_model(df):
    model = load_model()
    print(df)
    df = normalisedf(df)
    prediction = model.predict(df)
    return prediction

X_manual = pd.DataFrame([{
    "Time":"11:30:00 AM",
    "Date": 17,
    "Day of the week": "Thursday",
    "CarCount": 15,
    "BikeCount":100,
    "BusCount": 20,
    "TruckCount": 4,
    "Total": 139,
    "Weekend": False,
    "Hour": 12,
}])

# # # Ensure categorical columns are treated correctly if necessary
# # X_manual["Day of the week"] = X_manual["Day of the week"].astype("category")
print(run_model(X_manual))