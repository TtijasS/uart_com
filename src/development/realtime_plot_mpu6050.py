import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM7', 3000000, timeout=1)  # Replace 'COM7' with your serial port

# Configuration
buffer_size = 500  # Number of most recent samples to display
update_interval = 100  # Update on every 50th new sample

# Initialize data buffers
plot_buffer = np.zeros((buffer_size, 3))
counter = 0

# Initialize plot
fig, ax = plt.subplots()
ln1, = plt.plot([], [], 'r-', label='X-axis')
ln2, = plt.plot([], [], 'g-', label='Y-axis')
ln3, = plt.plot([], [], 'b-', label='Z-axis')

def init():
    ax.set_xlim(0, buffer_size)
    ax.set_ylim(-10, 10)  # Adjust the limits based on your expected data range
    return ln1, ln2, ln3

def read_serial_data():
    global counter, plot_buffer
    new_data = []
    buffer = b''

    while True:
        buffer += ser.read(ser.in_waiting or 1)
        if b'\n\r' in buffer:
            packets = buffer.split(b'\n\r')
            for packet in packets[:-1]:
                if len(packet) == 12:  # 3 floats * 4 bytes per float
                    x, y, z = struct.unpack('fff', packet)  # Unpack floats
                    new_data.append([x, y, z])
                    # print(x,y,z)
            buffer = packets[-1]
        
        if len(new_data) >= update_interval:
            break

    if len(new_data) > 0:
        new_data = np.array(new_data)
        plot_buffer = np.roll(plot_buffer, -len(new_data), axis=0)
        plot_buffer[-len(new_data):] = new_data
        update_plot()

def update_plot():
    ln1.set_data(np.arange(buffer_size), plot_buffer[:, 0])
    ln2.set_data(np.arange(buffer_size), plot_buffer[:, 1])
    ln3.set_data(np.arange(buffer_size), plot_buffer[:, 2])
    ax.figure.canvas.draw()

def update(frame):
    read_serial_data()
    return ln1, ln2, ln3

ani = FuncAnimation(fig, update, frames=np.arange(0, buffer_size),
                    init_func=init, blit=True, interval=100)  # Update every 200 ms

plt.legend()
plt.xlabel('Sample')
plt.ylabel('Acceleration')
plt.title('Real-time Accelerometer Data')
plt.show()
