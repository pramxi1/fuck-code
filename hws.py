# HWS no
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def run():
    # โหลดข้อมูลจากไฟล์ CSV
    df = pd.read_csv("7.csv")

    # แปลงคอลัมน์ 'Date' เป็นชนิดข้อมูล datetime
    df["date"] = pd.to_datetime(df["date"])

    # สร้างโมเดล Holt-Winters ด้วยฤดูกาล
    model = ExponentialSmoothing(
        df["sale"], seasonal_periods=4, trend="add", seasonal="add"
    )

    # ฟิตโมเดล
    model_fit = model.fit()

    # ทำนายสำหรับ 12 เดือนถัดไป
    forecast = model_fit.forecast(steps=5)

    return forecast
