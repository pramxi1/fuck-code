import pandas as pd
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    # อ่านข้อมูลจาก URL
    data = pd.read_csv("./uploads/data.csv")

    # ตรวจสอบและแก้ไขข้อผิดพลาดที่เกิดขึ้นเมื่อมีเครื่องหมาย ',' ในข้อมูล
    try:
        # พยายามแปลงข้อมูลในคอลัมน์ 'sale' เป็น float
        data["sale"] = data["sale"].astype(float)
    except ValueError as e:
        # หากเกิดข้อผิดพลาด ValueError: could not convert string to float: '3,977.33' ใช้การแทนที่ด้วยการลบเครื่องหมาย ',' และแปลงเป็น float
        data["sale"] = data["sale"].str.replace(",", "").astype(float)
        print("Handled the ValueError by removing commas.")

    # แปลงข้อมูลเป็นรูปแบบ datetime
    data["date"] = pd.to_datetime(
        data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce"
    )

    # ตั้งค่า index เป็นวันที่
    data.set_index("date", inplace=True)

    # ตั้งค่า index เป็นวันที่และระบุความถี่ของข้อมูลเป็น "D" (วันละครั้ง)
    data.index.freq = "D"

    # สร้างโมเดล Holt-Winters' Exponential Smoothing
    model = ExponentialSmoothing(
        data["sale"],
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="legacy-heuristic",
    )

    # ฟิตโมเดล
    result = model.fit()

    # ทำนายค่าสำหรับข้อมูลในอนาคต
    forecast = result.forecast(12)

    # convert forecast series to dataframe
    df = forecast.to_frame(name="HWS").reset_index()
    # df.columns = ["date", "sale"]

    # # Adding the HWS column (3-day moving average)
    # df["HWS"] = df["sale"].rolling(window=3).mean()

    # พล็อตข้อมูลและผลการทำนาย
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["sale"], label="Actual")
    plt.plot(forecast.index, forecast, label="Forecast", color="red")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Holt-Winters' Exponential Smoothing Forecast")
    plt.legend()
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()

    return plot_data, df.tail(12)
