import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter
import os

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    df = pd.read_csv("./uploads/data.csv")

    # ตรวจสอบและแก้ไขข้อผิดพลาดที่เกิดขึ้นเมื่อมีเครื่องหมาย ',' ในข้อมูล #แก้
    try:
        # พยายามแปลงข้อมูลในคอลัมน์ 'sale' เป็น float
        df["sale"] = df["sale"].astype(float)
    except ValueError as e:
        # หากเกิดข้อผิดพลาด ValueError: could not convert string to float: '3,977.33' ใช้การแทนที่ด้วยการลบเครื่องหมาย ',' และแปลงเป็น float
        df["sale"] = df["sale"].str.replace(",", "").astype(float)

    # แปลงคอลัมน์ 'ds' ให้เป็น datetime
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")

    # df.set_index('date', inplace=True)

    # Calculate Simple Moving Average (SMA)
    window_size = 3  # You can adjust the window size as needed
    df["SMA"] = df["sale"].rolling(window=window_size).mean()
    
    # Plot the data and SMA
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df["sale"], label="Original")
    plt.plot(
        df.index,
        df["SMA"],
        label=f"SMA ({window_size}-day)",
        linestyle="--",
        color="red",
    )
    plt.title("simple moving average (SMA)")
    # ตั้งค่ารูปแบบวันที่ในแกน x
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))

    # หมุนข้อความวันที่ในแกน x เพื่อให้อ่านง่ายขึ้น
    plt.gcf().autofmt_xdate()

    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    
    df["date"] = df["date"].dt.strftime("%d/%m/%Y")
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    
    # **✅ บันทึกไฟล์รูปภาพ**
    output_dir = "uploads"
    os.makedirs(output_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี
    plot_file = os.path.join(output_dir, "forecast_plot.png")
    plt.savefig(plot_file, format="png")  # บันทึกไฟล์
    print(f"✅ Plot saved: {plot_file}")

    print(df)
    return plot_data, df
