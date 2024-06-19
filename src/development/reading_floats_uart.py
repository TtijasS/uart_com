import serial
import struct
import time

# Serial port configuration (adjust as necessary)
ser = serial.Serial('COM7', 3000000, timeout=1)  # Replace 'COM7' with your serial port

start = False
data_list = []
delimiter = b'\xfe\xfe\xfe\xfe'
buffer = bytearray()

ser.reset_input_buffer()  # Clear input buffer before reading data

def mlx_read_delimiter():
    global start, buffer
    while ser.in_waiting > 0 and not start:
        buffer.extend(ser.read(1))  # Read data byte-by-byte
        # Search for the delimiter in the buffer
        if delimiter in buffer:
            start = True
            # Attempt to decode buffer before the delimiter
            # try:
            #     decoded_message = buffer[:buffer.index(delimiter)].decode('utf-8')
            #     print("Decoded message:", decoded_message)
            # except UnicodeDecodeError as e:
            #     print(f"Error decoding message: {e}")
            # Remove everything up to and including the delimiter
            buffer = buffer[buffer.index(delimiter) + len(delimiter):]

def mlx_read_data_frame():
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
                data_list = []
                buffer = bytearray()  # Clear buffer after successful frame read

def find_deltatime(samples):
    new_data = []
    buffer = bytearray()

    timer_start = time.time()  # Start the timer before the loop begins
    while True:
        buffer.extend(ser.read(ser.in_waiting or 1))
        if b'\t' in buffer:
            packets = buffer.split(b'\t')
            for packet in packets[:-1]:
                if len(packet) == 12:  # 3 floats * 4 bytes per float
                    x, y, z = struct.unpack('fff', packet)  # Unpack floats
                    new_data.append([x, y, z])
                    # print(x, y, z)
            buffer = packets[-1]
        if len(new_data) >= samples:
            break
    
    timer_end = time.time()  # Stop the timer after collecting the samples
    total_time = timer_end - timer_start
    dt_per_sample = (total_time * 1000) / samples  # Calculate delta time per sample in milliseconds

    print(f"Number of samples taken: {len(new_data)}")
    print(f"Total time taken: {total_time:.8f} seconds")
    print(f"Delta time per sample: {dt_per_sample:.8f} milliseconds")
        

# Example usage
while True:
    # mlx_read_delimiter()
    # mlx_read_data_frame()
    find_deltatime(1000)
