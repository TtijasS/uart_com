import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM7', 3000000, timeout=1)  # Replace 'COM7' with your serial port

def read_serial_data():
    # Clear the input buffer
    ser.reset_input_buffer()
    # sleep 4 s
    time.sleep(4)

    while True:
        # Read all available bytes from the serial port
        if ser.in_waiting > 0:
            received_data = ser.read(ser.in_waiting)
            # Process the received data as floats
            for i in range(0, len(received_data) - 3, 4):
                float_bytes = received_data[i:i+4]
                if len(float_bytes) == 4:
                    data_buffer = struct.unpack('f', float_bytes)[0]
                    print(data_buffer)
                else:
                    print("Received data size mismatch")

# Example usage
while True:
    read_serial_data()
