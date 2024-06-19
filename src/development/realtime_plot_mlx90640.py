import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM7', 3000000, timeout=1)  # Replace 'COM7' with your serial port

start = False
data_list = []
delimiter = b'\xfe\xfe\xfe\xfe'
buffer = bytearray()

def read_delimiter():
    global start, buffer
    while ser.in_waiting > 0 and not start:
        buffer.extend(ser.read(1))  # Read data byte-by-byte
        # Search for the delimiter in the buffer
        if delimiter in buffer:
            start = True
            # Remove everything up to and including the delimiter
            
            buffer = buffer[buffer.index(delimiter) + len(delimiter):]

def read_data_frame():
    global start, data_list, buffer
    if start:
        while len(buffer) < 4 * 768:
            buffer.extend(ser.read(4 * 768 - len(buffer)))  # Read remaining bytes needed for the frame
        # Extract the entire frame of float values from the buffer
        if len(buffer) >= 4 * 768:
            data_bytes = buffer[:4 * 768]
            buffer = buffer[4 * 768:]
            data_list = struct.unpack('f' * 768, data_bytes)
            if len(data_list) == 768:
                start = False
                print("Received frame data:", data_list)

def update_frame(frame):
    read_delimiter()
    read_data_frame()
    if data_list:
        # Reshape the data to a 2D array (24x32 for MLX90640 sensor)
        data_array = np.array(data_list).reshape((24, 32))+6
        # apply gausian filter
        data_array = gaussian_filter(data_array, sigma=.7)
        ax.clear()
        cax = ax.imshow(data_array, cmap='jet', interpolation='nearest')
        if 'colorbar' not in update_frame.__dict__:
            update_frame.colorbar = fig.colorbar(cax, ax=ax, label='Temperature (°C)')
        else:
            update_frame.colorbar.update_normal(cax)
        ax.set_title('Thermal Image')
    else:
        print("No data to update")

# Set up the plot
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_frame, interval=200, cache_frame_data=False)  # Update every 200 ms

plt.show()
