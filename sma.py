import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io

matplotlib.use("Agg")  # Set the backend to non-interactive


def run():
    df = pd.read_csv("uploads/7.csv")
    # แปลงคอลัมน์ 'ds' ให้เป็น datetime
    df["date"] = pd.to_datetime(df["date"])

    # Set 'date' column as index
    df.set_index("date", inplace=True)

    # Calculate Simple Moving Average (SMA)
    window_size = 3  # You can adjust the window size as needed
    df["SMA"] = df["sale"].rolling(window=window_size).mean()

    # Plot the data and SMA
    plt.plot(df.index, df["sale"], label="Original")
    plt.plot(
        df.index,
        df["SMA"],
        label=f"SMA ({window_size}-day)",
        linestyle="--",
        color="red",
    )
    plt.title("SMA Plot")
    plt.xlabel("Date")
    plt.ylabel("Sale Amount")
    plt.legend()
    plt.grid(True)
    # Save the plot to a bytes buffer
    # buffer = io.BytesIO()
    img_path = os.path.join("model_img", "sma.png")

    # Save the plot to a file
    plt.savefig(img_path, format="png")

    # Close the plot
    plt.close()
    # plt.savefig(buffer, format="png")
    # buffer.seek(0)

    # Encode the plot image to base64
    # plot_data = base64.b64encode(buffer.getvalue()).decode()
    with open(img_path, "rb") as img_file:
        plot_data = base64.b64encode(img_file.read()).decode()

    # buffer.close()
    return plot_data, df
