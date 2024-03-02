import csv
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_csv('3.csv')

model = ExponentialSmoothing(df['sale'], seasonal_periods=4, seasonal='add')
fit_model = model.fit()

# ทำนายข้อมูลต่อไป 5 ชุด
forecast = fit_model.forecast(steps=5)
print(forecast)