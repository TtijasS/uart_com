import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM6', 115200, timeout=1)  # Replace 'COM6' with your serial port

# Configuration
buffer_size = 250 # number of most recent samples to display
update_interval = 50 # update on every 50th new sample

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
    ax.set_ylim(-0.3, 0.3)
    return ln1, ln2, ln3

def read_serial_data():
    global counter, plot_buffer
    new_data = []
    while ser.in_waiting > 0:
        received_data = ser.readline()
        data_buffer = received_data.decode('utf-8').replace('\r\n', '').split(';')
        data_buffer = list(map(float, data_buffer))
        new_data.extend(data_buffer)
        
        if len(new_data) >= 3 * update_interval:
            new_data = new_data[:3 * update_interval]  # Ensure the length matches the update_interval
            break
            
    if len(new_data) == 3 * update_interval:
        new_data = np.reshape(new_data, (update_interval, 3))
        plot_buffer = np.roll(plot_buffer, -update_interval, axis=0)
        plot_buffer[-update_interval:] = new_data
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
                    init_func=init, blit=True, interval=500)  # Update every 100 ms

plt.legend()
plt.xlabel('Sample')
plt.ylabel('Acceleration')
plt.title('Real-time Accelerometer Data')
plt.show()
