import os
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    df = pd.read_csv("uploads/7.csv")

    # แปลงคอลัมน์ 'Date' เป็นชนิดข้อมูล datetime
    df["date"] = pd.to_datetime(df["date"])

    # คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือน (3-month moving average)
    df["3_month_MA_1"] = df["sale"].rolling(window=3).mean()

    df["3_month_MA_1"] = df["3_month_MA_1"].shift(1)

    # บันทึกไฟล์ CSV หลังจากเลื่อนคอลัมน์
    df.to_csv("your_updated_file.csv", index=False)

    # คำนวณเฉลี่ยเคลื่อนที่ในระยะเวลา 3 เดือนของเฉลี่ยเคลื่อนที่ก่อนหน้า
    df["3_month_MA_2"] = df["3_month_MA_1"].rolling(window=3).mean()

    # แสดงผลลัพธ์
    df["Y_pred"] = 0.00

    df["Y_pred"] = (
        df["3_month_MA_1"].shift(-2) * 2
        - df["3_month_MA_2"].shift(-2)
        + (2 / (3 - 1)) * (df["3_month_MA_1"].shift(-2) - df["3_month_MA_2"].shift(-2))
    )
    df["Y_pred"] = df["Y_pred"].shift(2)

    # Calculate the short and long moving averages
    short_window = 3  # You can adjust the short window size as needed
    long_window = 6  # You can adjust the long window size as needed

    df["Short_MA"] = df["sale"].rolling(window=short_window).mean()
    df["Long_MA"] = df["sale"].rolling(window=long_window).mean()
    # Plot the data and DMA
    plt.plot(df.index, df["sale"], label="Original")
    plt.plot(
        df.index,
        df["Short_MA"],
        label=f"Short MA ({short_window}-day)",
        linestyle="--",
        color="red",
    )
    plt.plot(
        df.index,
        df["Long_MA"],
        label=f"Long MA ({long_window}-day)",
        linestyle="--",
        color="blue",
    )
    plt.title("DMA Plot")
    plt.xlabel("Date")
    plt.ylabel("Sale Amount")
    plt.legend()
    plt.grid(True)
    img_path = os.path.join("model_img", "dma.png")

    plt.savefig(img_path, format="png")

    # Close the plot
    plt.close()
    with open(img_path, "rb") as img_file:
        plot_data = base64.b64encode(img_file.read()).decode()

    return plot_data, df
