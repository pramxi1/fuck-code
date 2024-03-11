import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def run():
    df = pd.read_csv("7.csv")

    model = ExponentialSmoothing(df["sale"], seasonal_periods=4, seasonal="add")
    fit_model = model.fit()

    # ทำนายข้อมูลต่อไป 5 ชุด
    forecast = fit_model.forecast(steps=5)
    return forecast
