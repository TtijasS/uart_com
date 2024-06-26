from azure.iot.device.aio import IoTHubDeviceClient

import random
import datetime
import time
import json
import asyncio

# Define connection string
connectionString = "HostName=eg-iot.azure-devices.net;DeviceId=iotmaxx;SharedAccessKey=3ZJ1GbrRWEIw4BsMUY8YAoziTcKC8sVn3AIoTMHssZ0="

async def sendToIotHub(data):
    try:
        # Create an instance of the IoT Hub Client class
        device_client = IoTHubDeviceClient.create_from_connection_string(connectionString)

        # Connect the device client
        await device_client.connect()

        #Send the message
        await device_client.send_message(data)
        print("Message sent to IoT Hub:", data)

        # Shutdown the client
        await device_client.shutdown()
        
    
    except Exception as e:
        print("Error:", str(e))

def main():
    # Run an infinite while loop to send data every 5 seconds
    while True:
        # Generate random value
        temperature = random.randint(20, 50)
        # Generate data packet
        data={
            "device_id":"edge-1",
            "temperature":temperature,
            "edge_time_stamp":str(datetime.datetime.now())
        }
        asyncio.run(sendToIotHub(data=json.dumps(data)))
        time.sleep(5)

if __name__ == '__main__':
    main()