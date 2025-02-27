import pandas as pd
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from matplotlib.dates import DateFormatter

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
    
    data['sale'] = data['sale'].interpolate()

    # สร้างโมเดล Holt-Winters' Exponential Smoothing
    model = ExponentialSmoothing(
        data["sale"],
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="legacy-heuristic",
    )

    # ฟิตโมเดล
    result = model.fit()

    # ทำนายค่าสำหรับข้อมูลในอนาคต
    forecast = result.forecast(30)
    
    # รีเซ็ต index ของข้อมูลจริงและแปลงรูปแบบวันที่
    data_reset = data.reset_index()
    data_reset.rename(columns={"sale": "HWS"}, inplace=True)
    data_reset['date'] = data_reset['date'].dt.strftime('%d/%m/%Y')  # แปลงรูปแบบวันที่
    
    forecast_df = pd.DataFrame({
        'date': forecast.index.strftime('%d/%m/%Y'),  # แปลงรูปแบบวันที่
        'HWS': forecast.values
    })

    # รวมข้อมูลจริงและข้อมูลพยากรณ์เข้าด้วยกัน
    
    df = pd.concat([data_reset, forecast_df], ignore_index=True)
    # df.columns = ["date", "sale"]

    # # Adding the HWS column (3-day moving average)
    # df["HWS"] = df["sale"].rolling(window=3).mean()

    # พล็อตข้อมูลและผลการทำนาย
    plt.figure(figsize=(10, 4))

    # พล็อตข้อมูลจริง
    plt.plot(data.index, data['sale'], label='Actual')

    # พล็อตข้อมูลพยากรณ์
    plt.plot(forecast.index, forecast, label='Forecast', color='red')

    # ตั้งค่ารูปแบบวันที่ในแกน x
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))

    # หมุนข้อความวันที่ในแกน x เพื่อให้ดูง่ายขึ้น
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
    print(df)
    return plot_data, df
