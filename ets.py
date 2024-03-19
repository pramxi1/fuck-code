import os
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import base64
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    df = pd.read_csv("uploads/7.csv")

    # สร้าง Exponential Smoothing State Space Model
    model = sm.tsa.ExponentialSmoothing(
        df["sale"], trend="add", seasonal="add", seasonal_periods=12
    )

    # ประมาณการพารามิเตอร์และฟิตโมเดล
    fit_model = model.fit()

    # ทำนายข้อมูล
    forecast = fit_model.forecast(steps=12)

    # พล็อตกราฟข้อมูลเดิมและการทำนาย
    plt.figure(figsize=(10, 6))
    plt.plot(df["sale"], label="Actual")
    plt.plot(fit_model.fittedvalues, label="Fitted")
    plt.plot(forecast, label="Forecast")
    plt.legend()

    img_path = os.path.join("model_img", "ets.png")

    plt.savefig(img_path, format="png")

    # Close the plot
    plt.close()
    with open(img_path, "rb") as img_file:
        plot_data = base64.b64encode(img_file.read()).decode()
    return plot_data, forecast
