import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM7', 3000000, timeout=1)  # Replace 'COM7' with your serial port
delimiter = b'\t'
buffer = bytearray()

# Configuration
buffer_size = 1024  # Number of samples for FFT
update_interval = 128  # Update on every n-th new sample

# Initialize data buffers
plot_buffer = np.zeros((buffer_size, 3))
counter = 0

# Initialize plot
fig, ax = plt.subplots()
ln, = plt.plot([], [], 'r-', label='X')

def init():
    ax.set_xlim(0, buffer_size//2)
    ax.set_ylim(0, 100)  # Adjust the limits based on your expected FFT magnitude range
    return ln,

def read_serial_data():
    global counter, plot_buffer, buffer
    new_data = []

    while True:
        buffer.extend(ser.read(ser.in_waiting))
        if b'\t' in buffer:
            packets = buffer.split(b'\t')
            for packet in packets[:-1]:
                if len(packet) == 12:  # 3 floats * 4 bytes per float
                    x, y, z = struct.unpack('fff', packet)  # Unpack floats
                    new_data.append([x, y, z])
            buffer = packets[-1]        
        if len(new_data) >= update_interval:
            break

    if len(new_data) > 0:
        new_data = np.array(new_data)
        plot_buffer = np.roll(plot_buffer, -len(new_data), axis=0)
        plot_buffer[-len(new_data):] = new_data
        update_plot()

def update_plot():
    x_data = plot_buffer[:, 0]
    fft_complex = np.fft.fft(x_data)  # Perform FFT
    fft_magnitude = np.abs(fft_complex)[:buffer_size//2]  # Take magnitude and half the spectrum
    ln.set_data(np.arange(buffer_size//2), fft_magnitude)
    ax.figure.canvas.draw()

def update(frame):
    read_serial_data()
    return ln,

ani = FuncAnimation(fig, update, frames=np.arange(0, buffer_size),
                    init_func=init, blit=True, interval=50)  # Update every x ms

plt.legend()
plt.xlabel('Frequency Bin')
plt.ylabel('Magnitude')
plt.title('Real-time FFT of X-axis Accelerometer Data')
plt.show()
