#HWS no
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv('3.csv')

# แปลงคอลัมน์ 'Date' เป็นชนิดข้อมูล datetime
df['date'] = pd.to_datetime(df['date'])

# สร้างโมเดล Holt-Winters ด้วยฤดูกาล
model = ExponentialSmoothing(df['sale'], seasonal_periods=4, trend='add', seasonal='add')

# ฟิตโมเดล
model_fit = model.fit()

# ทำนายสำหรับ 12 เดือนถัดไป
forecast = model_fit.forecast(steps=5)

# แสดงผลลัพธ์
print(forecast)