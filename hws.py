import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
import base64
import matplotlib

matplotlib.use("Agg")  # ใช้ non-interactive mode

def run():
    # โหลดข้อมูลจากไฟล์ CSV
    data = pd.read_csv("./uploads/data.csv")

    # แปลงคอลัมน์ sale เป็น float
    if data["sale"].dtype == 'O':  
        data["sale"] = data["sale"].str.replace(",", "").astype(float)
    else:
        data["sale"] = data["sale"].astype(float)

    # ตรวจสอบและกำจัดวันที่ซ้ำกัน
    data.drop_duplicates(subset=["date"], keep="first", inplace=True)

    # แปลงคอลัมน์ date เป็น datetime และตั้งเป็น index
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    data.set_index("date", inplace=True)
    
    # ตั้งค่าความถี่เป็นรายวัน และเติมค่าขาดหาย
    data = data.asfreq("D")
    data["sale"] = data["sale"].interpolate()

    # กำหนดค่าพารามิเตอร์
    alpha = 0.3  # ค่าระดับ
    beta = 0.1   # ค่าแนวโน้ม
    gamma = 0.1  # ค่าฤดูกาล
    seasonal_periods = 12  # รอบฤดูกาล (ถ้าข้อมูลเป็นรายเดือน)

    # สร้างคอลัมน์ใหม่
    data["Level"] = 0.0
    data["Trend"] = 0.0
    data["Seasonal"] = 1.0
    data["HWS_Forecast"] = data["sale"]  # กำหนดค่าเริ่มต้นให้เท่ากับค่า sale

    # ค่าตั้งต้นสำหรับแนวโน้ม (Trend)
    if len(data) > 1:
        data.iloc[0, data.columns.get_loc("Level")] = data.iloc[0]["sale"]
        data.iloc[0, data.columns.get_loc("Trend")] = data.iloc[1]["sale"] - data.iloc[0]["sale"]
    
    # กำหนดค่า Seasonal ให้เป็นค่าเฉลี่ยของรอบก่อนหน้า
    if len(data) >= seasonal_periods:
        for i in range(seasonal_periods):
            data.iloc[i, data.columns.get_loc("Seasonal")] = data.iloc[i]["sale"] / data["sale"].mean()

    # คำนวณค่า Holt-Winters' Exponential Smoothing
    for t in range(1, len(data)):
        if t >= seasonal_periods:
            # คำนวณค่า Level
            data.iloc[t, data.columns.get_loc("Level")] = (
                alpha * (data.iloc[t]["sale"] / data.iloc[t - seasonal_periods]["Seasonal"]) + 
                (1 - alpha) * (data.iloc[t-1]["Level"] + data.iloc[t-1]["Trend"])
            )
            
            # คำนวณค่า Trend
            data.iloc[t, data.columns.get_loc("Trend")] = (
                beta * (data.iloc[t]["Level"] - data.iloc[t-1]["Level"]) + 
                (1 - beta) * data.iloc[t-1]["Trend"]
            )
            
            # คำนวณค่า Seasonal
            data.iloc[t, data.columns.get_loc("Seasonal")] = (
                gamma * (data.iloc[t]["sale"] / data.iloc[t]["Level"]) + 
                (1 - gamma) * data.iloc[t - seasonal_periods]["Seasonal"]
            )
            
            # คำนวณค่าพยากรณ์
            data.iloc[t, data.columns.get_loc("HWS_Forecast")] = (
                (data.iloc[t, data.columns.get_loc("Level")] + data.iloc[t, data.columns.get_loc("Trend")]) * 
                data.iloc[t - seasonal_periods, data.columns.get_loc("Seasonal")]
            )
        else:
            # ก่อนถึงช่วง Seasonal Period ใช้ Level + Trend เป็น Forecast
            data.iloc[t, data.columns.get_loc("Level")] = (
                alpha * data.iloc[t]["sale"] + 
                (1 - alpha) * (data.iloc[t-1]["Level"] + data.iloc[t-1]["Trend"])
            )
            data.iloc[t, data.columns.get_loc("Trend")] = (
                beta * (data.iloc[t]["Level"] - data.iloc[t-1]["Level"]) + 
                (1 - beta) * data.iloc[t-1]["Trend"]
            )
            data.iloc[t, data.columns.get_loc("HWS_Forecast")] = (
                data.iloc[t]["Level"] + data.iloc[t]["Trend"]
            )
    
    # ปรับค่าทศนิยมให้เป็น 2 ตำแหน่ง
    data = data.round(3)

    # แก้ไขค่าที่อาจเป็น NaN หรือ Infinite
    data["HWS_Forecast"].replace([np.inf, -np.inf], np.nan, inplace=True)
    data["HWS_Forecast"].fillna(data["sale"].mean(), inplace=True)

    # คำนวณค่าความผิดพลาด
    error = data["sale"] - data["HWS_Forecast"]
    MSE = (error ** 2).mean()
    RMSE = np.sqrt(MSE)
    MAPE = (np.abs(error / data["sale"]) * 100).mean()

    print(f"MSE: {MSE:.2f}, RMSE: {RMSE:.2f}, MAPE: {MAPE:.2f}%")

    # พล็อตกราฟผลการพยากรณ์
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data["sale"], label="Actual")
    plt.plot(data.index, data["HWS_Forecast"], label="HWS Forecast", color="red")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title("Holt-Winters' Exponential Smoothing (Adjusted)")
    plt.legend()
    
    # บันทึกไฟล์รูป
    output_dir = "uploads"
    os.makedirs(output_dir, exist_ok=True)
    plot_file = os.path.join(output_dir, "forecast_plot.png")
    plt.savefig(plot_file, format="png")

    print(f"✅ HWS Plot saved: {plot_file}")

    # แปลงเป็น base64 สำหรับฝังในเว็บ
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return plot_data, data