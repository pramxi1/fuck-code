#DMA
import csv
import pandas as pd
# โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv('7.csv')

# แปลงคอลัมน์ 'Date' เป็นชนิดข้อมูล datetime
df['date'] = pd.to_datetime(df['date'])

# คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือน (3-month moving average)
df['3_month_MA_1'] = df['sale'].rolling(window=3).mean()

df['3_month_MA_1'] = df['3_month_MA_1'].shift(1)

# บันทึกไฟล์ CSV หลังจากเลื่อนคอลัมน์
df.to_csv('your_updated_file.csv', index=False)

# คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือนของเฉลี่ยเคลื่อนที่ก่อนหน้า
df['3_month_MA_2'] = df['3_month_MA_1'].rolling(window=3).mean()

# แสดงผลลัพธ์
df['Y_pred'] = 0.00

df['Y_pred'] = df['3_month_MA_1'].shift(-2) * 2 - df['3_month_MA_2'].shift(-2) + (2/(3-1)) * (df['3_month_MA_1'].shift(-2) - df['3_month_MA_2'].shift(-2))
df['Y_pred'] = df['Y_pred'].shift(2)
print(df)
