# import logging
# from azure.eventhub import EventHubConsumerClient

# connection_str = 'Endpoint=sb://ihsuprodamres117dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=WPE0GMmUi8YnzzX+uKXLC+dRkO2lYnM71AIoTL1PW1Q=;EntityPath=iothub-ehub-eg-iot-60160045-b0d83668a1'
# consumer_group = '$Default'
# client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group)

# logger = logging.getLogger("azure.eventhub")
# logging.basicConfig(level=logging.INFO)

# def on_event_batch(partition_context, events):
#     logger.info("Received event from partition {}".format(partition_context.partition_id))
#     partition_context.update_checkpoint()

# with client:
#     client.receive_batch(
#         on_event_batch=on_event_batch,
#         starting_position="-1",  # "-1" is from the beginning of the partition.
#     )

import logging
import asyncio
from azure.eventhub.aio import EventHubConsumerClient


connection_str = 'Endpoint=sb://ihsuprodamres117dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=WPE0GMmUi8YnzzX+uKXLC+dRkO2lYnM71AIoTL1PW1Q=;EntityPath=iothub-ehub-eg-iot-60160045-b0d83668a1'
consumer_group = '$Default'

logger = logging.getLogger("azure.eventhub")
logging.basicConfig(level=logging.INFO)

async def on_event_batch(partition_context, events):
    logger.info("Received event from partition {}".format(partition_context.partition_id))
    for event in events:
            print(event.body_as_str())
    await partition_context.update_checkpoint()

async def receive_batch():
    client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group)
    async with client:
        await client.receive_batch(
            on_event_batch=on_event_batch,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )
        # receive events from specified partition:
        # await client.receive_batch(on_event_batch=on_event_batch, partition_id='0')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(receive_batch())

