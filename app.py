import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
import pymannkendall as mk
import seasonal_test as s_test
import dma as dma
import sma as sma
import ets as ets
import hws as hws
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

app = Flask(__name__)
PORT = 8080

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# cached_plot_data = None
# html_table = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/requirement")
def requirement():
    return render_template("requirement.html")


@app.route("/import_file", methods=["GET", "POST"])
def import_file():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400
        if file:
            # session.pop('cached_plot_data', default=None)
            # session.pop('html_table', default=None)
            session["cached_plot_data"] = None
            session["html_table"] = None
            filename = "data.csv"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return render_template("import_file.html")


import matplotlib.pyplot as plt
from io import BytesIO
import base64
from statsmodels.tsa.seasonal import seasonal_decompose

@app.route("/trend")
def trend():
    trend_ = 0
    seasonal_ = 0

    # อ่านข้อมูลจากไฟล์ CSV
    df = pd.read_csv("./uploads/data.csv")

    try:
        # พยายามแปลงข้อมูลในคอลัมน์ 'sale' เป็น float
        df["sale"] = df["sale"].astype(float)
    except ValueError as e:
        # แก้ไขข้อมูลที่มีเครื่องหมาย ',' และแปลงเป็น float
        df["sale"] = df["sale"].str.replace(",", "").str.strip("").astype(float)

    x = df["sale"]

    # ทดสอบแนวโน้มด้วย Mann-Kendall Test
    trend_result = mk.original_test(x)
    
    print("Trend:", trend_result.trend)
    print("Hypothesis Test Result:", trend_result.h)
    print("p-value:", trend_result.p)
    print("z-score:", trend_result.z)

    if trend_result.trend in ["increasing", "decreasing"]:
        trend_ += 1

    # ทดสอบฤดูกาล (Seasonality Test)
    s_result = s_test.sk_test(x.values)

    if s_result.p < 0.05:
        seasonal_ += 1
        print("Seasonal: have Seasonal")
    # แยกส่วนประกอบของข้อมูลด้วย Seasonal Decomposition
    decomposition = seasonal_decompose(x, model="additive", period=12)

    # สร้างกราฟแนวโน้ม
    trend_fig = plt.figure(figsize=(14, 6))
    plt.plot(df.index, x, label="Original Data")
    plt.plot(df.index, decomposition.trend, label="Trend", color="orange", linewidth=2)
    plt.legend()
    plt.title("Trend Analysis")
    plt.xlabel("Index")
    plt.ylabel("Sale")
    plt.grid()
    
    # ตั้งค่ารูปแบบวันที่ในแกน X
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m/%Y"))  # แสดงวันที่ในรูปแบบ DD/MM/YYYY
    plt.gcf().autofmt_xdate()  # หมุนวันที่เพื่อไม่ให้ทับกัน

    # แปลงกราฟเป็น base64 เพื่อฝังใน HTML
    trend_img = BytesIO()
    plt.savefig(trend_img, format="png")
    trend_img.seek(0)
    trend_base64 = base64.b64encode(trend_img.getvalue()).decode()

    # สร้างกราฟฤดูกาล
    seasonal_fig = plt.figure(figsize=(14, 6))
    plt.plot(decomposition.seasonal, label="Seasonality", color="green")
    plt.title("Seasonality Analysis")
    plt.xlabel("Index")
    plt.ylabel("Seasonal Effect")
    plt.grid()
    
    # ตั้งค่ารูปแบบวันที่ในแกน X
    ax = plt.gca()
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m/%Y"))  # แสดงวันที่ในรูปแบบ DD/MM/YYYY
    plt.gcf().autofmt_xdate()  # หมุนวันที่เพื่อไม่ให้ทับกัน

    # แปลงกราฟเป็น base64 เพื่อฝังใน HTML
    seasonal_img = BytesIO()
    plt.savefig(seasonal_img, format="png")
    seasonal_img.seek(0)
    seasonal_base64 = base64.b64encode(seasonal_img.getvalue()).decode()

    # Render HTML พร้อมส่งผลลัพธ์และกราฟ
    session["trend"] = trend_
    session["seasonal"] = seasonal_
    return render_template(
        "trend_and_seasonal_testing.html",
        trend_result=trend_result,
        s_result=s_result,
        trend_graph=trend_base64,
        seasonal_graph=seasonal_base64,
    )


@app.route("/model")
def model():
    cached_plot_data = session["cached_plot_data"]
    html_table = session["html_table"]
    # Retrieve values from session
    trend_ = session.get("trend", 0)
    seasonal_ = session.get("seasonal", 0)

    print(cached_plot_data, html_table)
    if cached_plot_data is None:
        if trend_ > 0 and seasonal_ > 0:
            # hws
            result, df = hws.run()
            # print(result)
        elif trend_ > 0 and seasonal_ == 0:
            # dma
            result, df = dma.run()
            # print(result)
        elif trend_ == 0 and seasonal_ > 0:
            # ets
            result, df = ets.run()
            # print(result)
        else:
            # sma
            result, df = sma.run()
            # print(result)
        cached_plot_data = result
        # Convert DataFrame to HTML table
        html_table = df.to_html(index=False)
    session["cached_plot_data"] = cached_plot_data
    session["html_table"] = html_table
    return render_template(
        "forecast.html", result=cached_plot_data, html_table=html_table
    )

@app.route("/model2")
def model2():
    cached_plot_data = session["cached_plot_data"]
    html_table = session["html_table"]
    # Retrieve values from session
    trend_ = session.get("trend", 0)
    seasonal_ = session.get("seasonal", 0)

    print(cached_plot_data, html_table)
    if cached_plot_data is None:
        if trend_ > 0 and seasonal_ > 0:
            # hws
            result, df = hws.run()
            # print(result)
        elif trend_ > 0 and seasonal_ == 0:
            # dma
            result, df = dma.run()
            # print(result)
        elif trend_ == 0 and seasonal_ > 0:
            # ets
            result, df = ets.run()
            # print(result)
        else:
            # sma
            result, df = sma.run()
            # print(result)
        cached_plot_data = result
        # Convert DataFrame to HTML table
        html_table = df.to_html(index=False)
    session["cached_plot_data"] = cached_plot_data
    session["html_table"] = html_table
    return render_template(
        "forecast_table.html", result=cached_plot_data, html_table=html_table
    )

if __name__ == "__main__":
    print("Starting server on port", PORT)
    app.run(port=PORT)
