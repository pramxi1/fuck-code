import pandas as pd
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from matplotlib.dates import DateFormatter
import os

matplotlib.use("Agg")  # Set the backend to non-interactive

def run():
    # อ่านข้อมูลจาก CSV
    data = pd.read_csv("./uploads/data.csv")

    # แปลงคอลัมน์ sale เป็น float
    if data["sale"].dtype == 'O':  
        data["sale"] = data["sale"].str.replace(",", "").astype(float)
    else:
        data["sale"] = data["sale"].astype(float)

    # แปลงข้อมูล date เป็น datetime
    data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")

    # ตั้งค่า index เป็น date
    data.set_index("date", inplace=True)
    
    # ตั้งค่าความถี่เป็นรายวัน และเติมค่าที่ขาดหายไป
    data = data.asfreq("D")
    data["sale"] = data["sale"].interpolate()

    # สร้างโมเดล Holt-Winters' Exponential Smoothing
    model = ExponentialSmoothing(
        data["sale"],
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated",
    )

    # ฟิตโมเดล
    result = model.fit()

    # ทำนายค่าสำหรับ 30 วันข้างหน้า
    forecast = result.forecast(30)

    # รีเซ็ต index และแปลงวันที่ให้เป็น String
    data_reset = data.reset_index()
    data_reset["date"] = data_reset["date"].dt.strftime('%d/%m/%Y')

    # ✅ ตรวจสอบว่า 'sale' มีอยู่ใน DataFrame จริงหรือไม่
    if "sale" not in data_reset.columns:
        print("❌ Warning: 'sale' column missing in data_reset!")

    # ✅ สร้าง DataFrame ของค่าสำหรับอนาคต
    forecast_df = pd.DataFrame({
        "date": forecast.index.strftime('%d/%m/%Y'),
        "sale": None,  # ไม่มีค่าขายจริงในอนาคต
        "HWS": forecast.values
    })

    # ✅ เติมค่า NaN ใน HWS ด้วยค่าเฉลี่ยของ sale
    forecast_df["HWS"].fillna(data_reset["sale"].mean(), inplace=True)

    # ✅ รวมข้อมูลจริงและข้อมูลพยากรณ์
    df = pd.concat([data_reset, forecast_df], ignore_index=True)

    # ✅ ตรวจสอบว่าคอลัมน์ 'sale' มีอยู่หรือไม่
    if "sale" not in df.columns:
        print("❌ Warning: 'sale' column is missing after concatenation!")
        df = df.merge(data_reset[["date", "sale"]], on="date", how="left")
        print("✅ 'sale' column added back from data_reset.")

    print(f"✅ DataFrame Columns: {df.columns}")
    print(f"✅ First 5 rows of df:\n{df.head()}")

    # พล็อตข้อมูลและผลการทำนาย
    plt.figure(figsize=(10, 4))

    # พล็อตข้อมูลจริง
    plt.plot(data.index, data['sale'], label='Actual')

    # พล็อตข้อมูลพยากรณ์
    plt.plot(forecast.index, forecast, label='Forecast', color='red')

    # ตั้งค่ารูปแบบวันที่ในแกน x
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
    plt.gcf().autofmt_xdate()

    # เพิ่มรายละเอียดในกราฟ
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Holt-Winters\' Exponential Smoothing Forecast')
    plt.legend()
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    
    # บันทึกไฟล์ภาพพยากรณ์ใหม่
    output_dir = "uploads"
    os.makedirs(output_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี
    plot_file = os.path.join(output_dir, "forecast_plot.png")
    plt.savefig(plot_file, format="png")  # บันทึกไฟล์
    print(f"✅ HWS Plot saved: {plot_file}")

    return plot_data, df