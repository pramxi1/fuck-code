# HWS no
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import base64
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive

# อ่านข้อมูลจาก URL
data = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/a10.csv")


def run():
    # โหลดข้อมูลจากไฟล์ CSV
    df = pd.read_csv("uploads/7.csv")

    # แปลงข้อมูลเป็นรูปแบบ datetime
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # ตั้งค่า index เป็นวันที่
    df.set_index("date", inplace=True)

    # # สร้างโมเดล Holt-Winters ด้วยฤดูกาล
    # model = ExponentialSmoothing(
    #     df["sale"], seasonal_periods=4, trend="add", seasonal="add"
    # )

    # # ฟิตโมเดล
    # model_fit = model.fit()

    # # ทำนายสำหรับ 12 เดือนถัดไป
    # forecast = model_fit.forecast(steps=5)

    # สร้างโมเดล Holt-Winters' Exponential Smoothing
    model = ExponentialSmoothing(
        df["sale"], trend="add", seasonal="add", seasonal_periods=12
    )

    # ฟิตโมเดล
    result = model.fit()

    # ทำนายค่าสำหรับข้อมูลในอนาคต
    forecast = result.forecast(12)

    # พล็อตข้อมูลและผลการทำนาย
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["sale"], label="Actual")
    plt.plot(forecast.index, forecast, label="Forecast", color="red")
    plt.xlabel("Date")
    plt.ylabel("sale")
    plt.title("Holt-Winters' Exponential Smoothing Forecast")
    plt.legend()

    img_path = os.path.join("model_img", "hws.png")

    plt.savefig(img_path, format="png")

    # Close the plot
    plt.close()
    with open(img_path, "rb") as img_file:
        plot_data = base64.b64encode(img_file.read()).decode()
    return plot_data, forecast
