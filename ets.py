#ETS Yes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/a10.csv')

# สร้าง Exponential Smoothing State Space Model
model = sm.tsa.ExponentialSmoothing(df['value'], trend='add', seasonal='add', seasonal_periods=12)

# ประมาณการพารามิเตอร์และฟิตโมเดล
fit_model = model.fit()

# ทำนายข้อมูล
forecast = fit_model.forecast(steps=5)

# พล็อตกราฟข้อมูลเดิมและการทำนาย
plt.figure(figsize=(10, 6))
plt.plot(df['value'], label='Actual')
plt.plot(fit_model.fittedvalues, label='Fitted')
plt.plot(forecast, label='Forecast')
plt.legend()
plt.show()

# สร้าง DataFrame ของการทำนาย
forecast_df = pd.DataFrame({'date': pd.date_range(start=df['date'].iloc[-1], periods=5, freq='M', closed='right'),
                            'Forecast': forecast})

# แสดงตารางข้อมูล
display(forecast_df)

# บันทึกตารางข้อมูลเป็นไฟล์ CSV
forecast_df.to_csv('forecast_data.csv', index=False)