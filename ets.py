# ETS Yes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import io
import base64
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    # อ่านข้อมูลจากไฟล์ CSV
    df = pd.read_csv("./uploads/data.csv")

    try:
        # พยายามแปลงข้อมูลในคอลัมน์ 'sale' เป็น float
        df["sale"] = df["sale"].astype(float)
    except ValueError as e:
        # หากเกิดข้อผิดพลาด ValueError: could not convert string to float: '3,977.33' ใช้การแทนที่ด้วยการลบเครื่องหมาย ',' และแปลงเป็น float
        df["sale"] = df["sale"].str.replace(",", "").astype(float)

    # สร้าง Exponential Smoothing State Space Model
    model = sm.tsa.ExponentialSmoothing(
        df["value"], trend="add", seasonal="add", seasonal_periods=12
    )

    # ประมาณการพารามิเตอร์และฟิตโมเดล
    fit_model = model.fit()

    # ทำนายข้อมูล
    forecast = fit_model.forecast(steps=12)

    # พล็อตกราฟข้อมูลเดิมและการทำนาย
    plt.figure(figsize=(10, 6))
    plt.plot(df["value"], label="Actual")
    plt.plot(fit_model.fittedvalues, label="Fitted")
    plt.plot(forecast, label="Forecast")
    plt.title("Exponential Smoothing State Space Model (ETS)")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    return plot_data, df.tail(12)
