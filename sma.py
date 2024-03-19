import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive

def run():
    df = pd.read_csv("7.csv")
    # แปลงคอลัมน์ 'ds' ให้เป็น datetime
    df["date"] = pd.to_datetime(df["date"])

    # คำนวณค่า Simple Moving Average (SMA) โดยใช้ช่วงเวลา 4 วัน
    window_size = 3
    df["SMA"] = df["sale"].rolling(window=window_size).mean()

    df.set_index('date', inplace=True)

    # Calculate Simple Moving Average (SMA)
    window_size = 3  # You can adjust the window size as needed
    df['SMA'] = df['sale'].rolling(window=window_size).mean()

    # Plot the data and SMA
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['sale'], label='Original')
    plt.plot(df.index, df['SMA'], label=f'SMA ({window_size}-day)', linestyle='--', color='red')
    plt.title('SMA Plot')
    plt.xlabel('Date')
    plt.ylabel('Sale Amount')
    plt.legend()
    plt.grid(True)
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    return plot_data, df
    