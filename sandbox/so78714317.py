import logging
logging.basicConfig(level=logging.DEBUG)

# import serial
import matplotlib.pyplot as plt

# from matplotlib.animation import FuncAnimation, FFMpegWriter
import ffmpegio as ff

from datetime import datetime, timedelta
import numpy as np
import schedule
import time

# Constants
GRAVITY = 9.81  # Standard gravity in m/s²

# Initialize serial connections to HC-06 devices
# ser_x_accel = serial.Serial('COM4', 9600, timeout=1)  # X-axis acceleration data
# ser_y_angle = serial.Serial('COM11', 9600, timeout=1)  # Y-axis angle data

# Initialize empty lists to store data
x_accel_data = []
y_angle_data = []
timestamps = []

# Initialize Excel workbook
# wb = openpyxl.Workbook()
# ws = wb.active
# ws.title = "Sensor Data"
# ws.append(["Timestamp", "X Acceleration (m/s²)", "Y Angle (degrees)"])


# Function to update the plot and log data
def update(f):
    # Read data from serial connections
    line_x_accel = np.random.randn(1)  # ser_x_accel.readline().decode('utf-8').strip()
    line_y_angle = np.random.randn(1)  # ser_y_angle.readline().decode('utf-8').strip()

    try:
        # Parse and process X-axis acceleration data
        x_accel_g = float(line_x_accel)  # Acceleration in g read from serial
        x_accel_ms2 = x_accel_g * GRAVITY  # Convert from g to m/s²
        x_accel_data.append(x_accel_ms2)

        # Parse and process Y-axis angle data
        y_angle = float(line_y_angle)
        y_angle_data.append(y_angle)

        # Append timestamp
        timestamps.append(datetime.now())

        # Limit data points to show only the latest 100
        if len(x_accel_data) > 100:
            x_accel_data.pop(0)
            y_angle_data.pop(0)
            timestamps.pop(0)

        # Log data to Excel with timestamp
        # timestamp_str = timestamps[-1].strftime("%H:%M:%S")
        # ws.append([timestamp_str, x_accel_data[-1], y_angle_data[-1]])

        # Clear and update plots
        ax1.clear()
        ax1.plot(timestamps, x_accel_data, label="X Acceleration", color="b")
        ax1.legend(loc="upper left")
        ax1.set_ylim([-20, 20])  # Adjust based on expected acceleration range in m/s²
        ax1.set_title("Real-time X Acceleration Data")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Acceleration (m/s²)")
        ax1.grid(True)

        ax2.clear()
        ax2.plot(timestamps, y_angle_data, label="Y Angle", color="g")
        ax2.legend(loc="upper left")
        ax2.set_ylim([-180, 180])
        ax2.set_title("Real-time Y Angle Data")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Angle (degrees)")
        ax2.grid(True)

        # Update text boxes with latest values
        text_box.set_text(f"X Acceleration: {x_accel_data[-1]:.2f} m/s²")
        text_box2.set_text(f"Y Angle: {y_angle_data[-1]:.2f}°")

        # Save the workbook periodically (every 100 updates)
        # if frame % 100 == 0:
        # wb.save("sensor_data.xlsx")

        # plt.draw()

        # print("update", datetime.now())
        f.write(fig)

    except ValueError:
        pass  # Ignore lines that are not properly formatted


# Setup the plots
# with plt.ion():
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
text_box = ax1.text(
    0.05,
    0.95,
    "",
    transform=ax1.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
)
text_box2 = ax2.text(
    0.05,
    0.95,
    "",
    transform=ax2.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
)

with ff.open(
    "sandbox/test.mp4|[f=mpegts]udp://127.0.0.1:1234?pkt_size=1316",
    "wv",
    rate_in=10,
    y=ff.FLAG,
    show_log=True,
    preset="ultrafast",
    tune="zerolatency",
    vcodec="libx264",
    map= '0:v',
    f="tee",
) as f:
    s = schedule.every(0.1)
    s.seconds.until(datetime.now() + timedelta(seconds=10)).do(
        update, f
    )  # minutes=1)

    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()
        time.sleep(0.1)

    print("schedule complete")

# # Animate the plots
# ani = FuncAnimation(fig, update, interval=100)  # Update interval of 100ms

# # Save the animation as a video file
# writer = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("sensor_data.mp4", writer=writer)

# plt.tight_layout()
# plt.show()
