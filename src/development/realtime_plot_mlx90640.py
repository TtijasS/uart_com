import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM6', 115200, timeout=1)  # Replace 'COM3' with your serial port

start_flag = False

print("Waiting for data...")


start = False
data_list = []

def read_serial_data():
    global start, data_list
    if ser.in_waiting > 0:
        received_data = ser.readline()
        
        # Check for start and end markers
        if received_data == b'1f\r\n':
            print("Start")
            start = True
            return
        elif received_data == b'f1\r\n':
            print("Stop")
            start = False
            return
        if start:
            data_buffer = received_data.decode('utf-8').replace('\r\n', '').split(';')
            if len(data_buffer) == 768:
                data_list = list(map(float, data_buffer))
                print("Data received and processed")
            else:
                print(f"Incomplete data received: {len(data_buffer)} items")

# Function to update the plot
def update(frame):
    read_serial_data()
    if data_list:
        # Reshape the data to a 2D array (24x32 for MLX90640 sensor)
        data_array = np.array(data_list).reshape((24, 32)) + 8
        ax.clear()
        cax = ax.imshow(data_array, cmap='jet', interpolation='nearest')
        if 'colorbar' not in update.__dict__:
            update.colorbar = fig.colorbar(cax, ax=ax, label='Temperature (°C)')
        else:
            update.colorbar.update_normal(cax)
        ax.set_title('Thermal Image')
    else:
        print("No data to update")

# Set up the plot
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, interval=10, cache_frame_data=False)  # Update every 200 ms

plt.show()
