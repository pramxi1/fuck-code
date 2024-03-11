import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # อ่านข้อมูลจากไฟล์ CSV
    df = pd.read_csv('7.csv')

    # แปลงข้อมูลเป็นรูปแบบที่ Javascript เข้าใจ
    dates = df['date'].tolist()
    sales = df['sale'].tolist()

    # เรนเดอร์เทมเพลต HTML พร้อมส่งข้อมูล
    return render_template('1.html', dates=dates, sales=sales)

if __name__ == '__main__':
    app.run()