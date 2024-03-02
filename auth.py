from flask import Blueprint, render_template
import csv
import pandas as pd
import numpy as np

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/hello')
def hello():
    df = pd.read_csv("7.csv")
    # แปลงคอลัมน์ 'ds' ให้เป็น datetime
    df["date"] = pd.to_datetime(df["date"])

    # คำนวณค่า Simple Moving Average (SMA) โดยใช้ช่วงเวลา 4 วัน
    window_size = int(input("Window_size :"))
    df["SMA"] = df["sale"].rolling(window=window_size).mean()

    # แสดงผลลัพธ์
    #print(df)
    message = df
    return render_template('test2.html', message=message)

