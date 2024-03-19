import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# อ่านข้อมูลจาก URL
data = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/a10.csv")

# แปลงข้อมูลเป็นรูปแบบ datetime
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

# ตั้งค่า index เป็นวันที่
data.set_index('date', inplace=True)

# สร้างโมเดล Holt-Winters' Exponential Smoothing
model = ExponentialSmoothing(data['value'], trend='add', seasonal='add', seasonal_periods=12)

# ฟิตโมเดล
result = model.fit()

# ทำนายค่าสำหรับข้อมูลในอนาคต
forecast = result.forecast(12)

# พล็อตข้อมูลและผลการทำนาย
plt.figure(figsize=(10,6))
plt.plot(data.index, data['value'], label='Actual')
plt.plot(forecast.index, forecast, label='Forecast', color='red')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Holt-Winters\' Exponential Smoothing Forecast')
plt.legend()
plt.show()
print(forecast)