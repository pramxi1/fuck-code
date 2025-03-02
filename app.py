import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, session, send_file
import pymannkendall as mk
import seasonal_test as s_test
import dma as dma
import sma as sma
import ets as ets
import hws as hws
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from statsmodels.tsa.seasonal import seasonal_decompose
from accuracy import calculate_mse, calculate_rmse, calculate_mape
from matplotlib.dates import DateFormatter

app = Flask(__name__)
PORT = 8080

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        df["sale"] = pd.to_numeric(df["sale"].str.replace(",", ""), errors='coerce')
        df.dropna(subset=["sale"], inplace=True)  # ลบค่า NaN ที่เกิดขึ้น

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
    trend_ = session.get("trend", 0)
    seasonal_ = session.get("seasonal", 0)

    if trend_ > 0 and seasonal_ > 0:
        result, df = hws.run()
        df.rename(columns={"HWS": "predictions"}, inplace=True)
    elif trend_ > 0 and seasonal_ == 0:
        result, df = dma.run()
        df.rename(columns={"DMA": "predictions"}, inplace=True)
    elif trend_ == 0 and seasonal_ > 0:
        result, df = ets.run()
        df.rename(columns={"ETS": "predictions"}, inplace=True)
    else:
        result, df = sma.run()
        df.rename(columns={"SMA": "predictions"}, inplace=True)

    session["predictions"] = df["predictions"].tolist()
    session["actual_values"] = df["sale"].tolist()
    session["dates"] = df["date"].tolist()

    return render_template("forecast.html", result=result, html_table=df.to_html(index=False))


@app.route("/model2")
def model2():
    trend_ = session.get("trend", 0)
    seasonal_ = session.get("seasonal", 0)

    if trend_ > 0 and seasonal_ > 0:
        result, df = hws.run()
        df.rename(columns={"HWS": "predictions"}, inplace=True)
    elif trend_ > 0 and seasonal_ == 0:
        result, df = dma.run()
        df.rename(columns={"DMA": "predictions"}, inplace=True)
    elif trend_ == 0 and seasonal_ > 0:
        result, df = ets.run()
        df.rename(columns={"ETS": "predictions"}, inplace=True)
    else:
        result, df = sma.run()
        df.rename(columns={"SMA": "predictions"}, inplace=True)

    session["predictions"] = df["predictions"].tolist()
    session["actual_values"] = df["sale"].tolist()
    session["dates"] = df["date"].tolist()

    return render_template("forecast_table.html", html_table=df.to_html(index=False))


@app.route("/forecast_accuracy")
def forecast_accuracy():
    predictions = session.get("predictions", [])
    actual_values = session.get("actual_values", [])

    print(f"📢 Predictions (before filtering NaN): {predictions[:10]}")
    print(f"📢 Actual Values (before filtering NaN): {actual_values[:10]}")

    if not predictions or not actual_values:
        print("❌ No predictions or actual values available.")
        return jsonify({"message": "No predictions or actual values available"}), 400

    # แปลงเป็น numpy array และลบค่าที่เป็น NaN
    predictions = np.array(predictions, dtype=np.float64)
    actual_values = np.array(actual_values, dtype=np.float64)

    # ✅ แทนค่าที่เป็น NaN ด้วยค่าเฉลี่ยของ actual_values
    predictions = np.nan_to_num(predictions, nan=np.nanmean(actual_values))

    # ตรวจสอบ NaN และลบแถวที่มี NaN ออก
    mask = ~np.isnan(predictions) & ~np.isnan(actual_values)
    predictions, actual_values = predictions[mask], actual_values[mask]

    print(f"✅ Predictions (after filtering NaN): {predictions[:10]}")
    print(f"✅ Actual Values (after filtering NaN): {actual_values[:10]}")

    if len(predictions) == 0 or len(actual_values) == 0:
        print("❌ No valid data after removing NaN.")
        return jsonify({"message": "No valid data available for accuracy calculation"}), 400

    mse_value = round(calculate_mse(predictions, actual_values), 3)
    mape_value = round(calculate_mape(predictions, actual_values), 3)
    rmse_value = round(calculate_rmse(predictions, actual_values), 3)

    return render_template(
        "forecast_accuracy.html",
        mse_value=mse_value,
        mape_value=mape_value,
        rmse_value=rmse_value,
    )


@app.route("/download_forecast")
def download_forecast():
    df_forecast = pd.DataFrame({
        "Date": session.get("dates", []),
        "Actual Sales": session.get("actual_values", []),
        "Predictions": session.get("predictions", [])
    })

    output_dir = "uploads"
    os.makedirs(output_dir, exist_ok=True)
    forecast_file = os.path.join(output_dir, "forecast_results.csv")
    df_forecast.to_csv(forecast_file, index=False)

    return send_file(forecast_file, as_attachment=True)


@app.route("/download_page")
def download_page():
    return render_template("download.html")

@app.route("/download_plot")
def download_plot():
    # ตรวจสอบว่ามีไฟล์รูปภาพพยากรณ์หรือไม่
    plot_file = "uploads/forecast_plot.png"  # ที่อยู่ของไฟล์รูป
    if not os.path.exists(plot_file):
        print("⚠️ No plot image found!")
        return jsonify({"message": "No plot image available"}), 400
    
    return send_file(plot_file, as_attachment=True)


if __name__ == "__main__":
    print("Starting server on port", PORT)
    app.run(port=PORT, debug=True)