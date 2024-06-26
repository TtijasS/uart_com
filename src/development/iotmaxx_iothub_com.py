import ssl
import os
import logging
from azure.iot.device.aio import IoTHubDeviceClient
import random
import datetime
import time
import json
import asyncio

# Set up initial logging (will be reconfigured in main)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define connection string
connectionString = "HostName=eg-iot.azure-devices.net;DeviceId=iotmaxx;SharedAccessKey=3ZJ1GbrRWEIw4BsMUY8YAoziTcKC8sVn3AIoTMHssZ0="

# Set the environment variable to use the custom CA bundle
os.environ['SSL_CERT_FILE'] = '/data_inactive/eg_sensors/custom_certs/ca-certificates.crt'

async def sendToIotHub(data):
    try:
        # Create an instance of the IoT Hub Client class
        device_client = IoTHubDeviceClient.create_from_connection_string(connectionString)

        # Connect the device client
        await device_client.connect()

        # Send the message
        await device_client.send_message(data)
        print("Message sent to IoT Hub:", data)

        # Shutdown the client
        await device_client.shutdown()

    except Exception as e:
        logging.error("Error in sending data to IoT Hub", exc_info=True)

def main(verbose=False):
    # Reconfigure logging based on verbose flag
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.CRITICAL)

    # Run an infinite while loop to send data every 5 seconds
    while True:
        # Generate random value
        temperature = random.randint(20, 50)
        # Generate data packet
        data = {
            "device_id": "edge-1",
            "temperature": temperature,
            "edge_time_stamp": str(datetime.datetime.now())
        }
        asyncio.run(sendToIotHub(data=json.dumps(data)))
        time.sleep(5)

if __name__ == '__main__':
    # Call main with verbose=True to enable detailed logging, or verbose=False to disable logging
    main(verbose=False)
