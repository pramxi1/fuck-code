import pandas as pd


def run():
    df = pd.read_csv("7.csv")
    # แปลงคอลัมน์ 'ds' ให้เป็น datetime
    df["date"] = pd.to_datetime(df["date"])

    # คำนวณค่า Simple Moving Average (SMA) โดยใช้ช่วงเวลา 4 วัน
    window_size = int(input("Window_size :"))
    df["SMA"] = df["sale"].rolling(window=window_size).mean()
    return df
