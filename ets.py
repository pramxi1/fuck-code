import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import io
import base64
import os
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive

def run():
    # อ่านข้อมูลจากไฟล์ CSV
    df = pd.read_csv("./uploads/data.csv")

    # ตรวจสอบและจัดการค่าขาดหายใน 'sale'
    df["sale"] = df["sale"].fillna(df["sale"].mean())  # แทนที่ค่าที่ขาดหายด้วยค่าเฉลี่ย

    try:
        # แปลงคอลัมน์ 'sale' เป็น float
        df["sale"] = df["sale"].astype(float)

        # ตรวจสอบค่าที่แปลงแล้ว
        if df["sale"].isnull().any():
            print("Warning: There are still NaN values in 'sale' after filling.")
            df["sale"].fillna(df["sale"].mean(), inplace=True)  # ถ้ามีค่า NaN ให้เติมค่าเฉลี่ย

        # ตรวจสอบการกรอกข้อมูล
        if len(df["sale"]) < 12:
            raise ValueError("Not enough data to apply seasonal periods of 12.")
        
        # สร้างโมเดล Exponential Smoothing
        model = sm.tsa.ExponentialSmoothing(df["sale"], trend="add", seasonal="add", seasonal_periods=4)  # เปลี่ยนเป็น 4 เพื่อทดสอบ

        # ฟิตโมเดล
        fit_model = model.fit()

        # ทำนายข้อมูล
        forecast = fit_model.forecast(steps=12)

        # ตรวจสอบผลลัพธ์
        if forecast.isnull().any():
            print("Forecast contains NaN values. This could be due to insufficient data.")
            forecast = [0] * 12  # แทนที่ NaN ด้วย 0

        # เพิ่มคอลัมน์ 'forecast' ใน DataFrame
        df["forecast"] = forecast

        # ตรวจสอบว่าโฟลเดอร์ 'uploads' มีอยู่หรือไม่ หากไม่มีให้สร้าง
        plot_dir = './static/uploads'
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)  # สร้างโฟลเดอร์ uploads หากไม่มี

        # พล็อตกราฟข้อมูลเดิมและการทำนาย
        plt.figure(figsize=(10, 4))
        plt.plot(df["sale"], label="Actual")
        plt.plot(fit_model.fittedvalues, label="Fitted")
        plt.plot(forecast, label="Forecast")
        plt.title("Exponential Smoothing State Space Model (ETS)")
        plt.xlabel("Date")
        plt.ylabel("Sale")
        plt.legend()

        # บันทึกไฟล์รูป
        plot_file = os.path.join(plot_dir, "forecast_plot.png")
        plt.savefig(plot_file, format="png")

        print(f"✅ ETS Plot saved: {plot_file}")

        # แปลงเป็น base64 สำหรับฝังในเว็บ
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        return plot_data, df

    except Exception as e:
        print(f"Error during model fitting or forecasting: {e}")
        df["forecast"] = np.nan  # กำหนดค่า NaN ในกรณีที่เกิดข้อผิดพลาด
        return "", df