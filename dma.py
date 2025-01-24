import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    df = pd.read_csv("./uploads/data.csv")
    df.dropna(axis=0, inplace=True)
    # แปลงคอลัมน์ 'Date' เป็นชนิดข้อมูล datetime
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")

    try:
        # พยายามแปลงข้อมูลในคอลัมน์ 'sale' เป็น float
        df["sale"] = df["sale"].astype(float)
    except ValueError as e:
        # หากเกิดข้อผิดพลาด ValueError: could not convert string to float: '3,977.33' ใช้การแทนที่ด้วยการลบเครื่องหมาย ',' และแปลงเป็น float
        df["sale"] = df["sale"].str.replace(",", "").astype(float)

    # คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือน (3-month moving average)
    df["SMA"] = df["sale"].rolling(window=3).mean()

    # บันทึกไฟล์ CSV หลังจากเลื่อนคอลัมน์
    df.to_csv("your_updated_file.csv", index=False)

    # คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือนของเฉลี่ยเคลื่อนที่ก่อนหน้า
    df["DMA"] = df["SMA"].rolling(window=3).mean()
    
    # Plot the data and DMA
    plt.figure(figsize=(10, 6))  # กำหนดขนาดของกราฟให้กว้างขึ้น
    plt.plot(df["date"], df["sale"], label="Actual", color='green')
    plt.plot(df["date"], df["SMA"], label="SMA", linestyle="--", color="red")
    plt.plot(df["date"], df["DMA"], label="DMA", linestyle="--", color="blue")

    # การปรับการแสดงผลวันที่ให้ไม่ทับกัน
    plt.xticks(rotation=45, ha='right')  # หมุนแกน X เพื่อให้วันที่แสดงได้ชัดเจน

    # เพิ่มชื่อหัวข้อและคำอธิบาย
    plt.title("Double Exponential Moving Average (DMA)", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Sale Value", fontsize=12)

    # แสดง legend
    plt.legend()

    # ปรับแต่งพื้นที่ว่างให้พอเหมาะ
    plt.tight_layout()

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the plot image to base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    print(df)
    return plot_data, df