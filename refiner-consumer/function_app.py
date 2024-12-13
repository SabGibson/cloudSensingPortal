import logging
import azure.functions as func
from azure.storage.queue import QueueClient
import os
from refine_logic import *

app = func.FunctionApp()

def process_queue_messages(queue_name, refinery_function, region_name):
    # Get connection string from environment variable
    connection_string = os.environ['STORAGE_CONNECT_STRING']
    
    # Create queue client
    queue_client = QueueClient.from_connection_string(
        connection_string,
        queue_name
    )
    
    # Get queue properties to check if there are messages
    properties = queue_client.get_queue_properties()
    message_count = properties.approximate_message_count
    
    if message_count > 0:
        logging.info(f"Found {message_count} messages in {region_name} queue")
        
        # Receive up to 32 messages at a time
        messages = queue_client.receive_messages(max_messages=32)
        
        for message in messages:
            try:
                # Process the message
                message_text = message.content
                refinery_function(message_text)
                
                # Delete the message after successful processing
                queue_client.delete_message(message)
                
                logging.info(f"Successfully processed and deleted message from {region_name} queue")
            except Exception as e:
                logging.error(f"Error processing message in {region_name} queue: {str(e)}")
    else:
        logging.info(f"{region_name} queue is empty. No messages to process.")

@app.function_name(name="TimerTriggerUK")
@app.timer_trigger(schedule="0 */20 * * * *", arg_name="timer")
def process_uk_queue(timer: func.TimerRequest):
    process_queue_messages(
        queue_name="amazonuk-queue",
        refinery_function=refineryUK,
        region_name="UK"
    )
    logging.info("UK queue processing complete!")

@app.function_name(name="TimerTriggerUS")
@app.timer_trigger(schedule="0 */20 * * * *", arg_name="timer")
def process_us_queue(timer: func.TimerRequest):
    process_queue_messages(
        queue_name="amazonus-queue",
        refinery_function=refineryUS,
        region_name="US"
    )
    logging.info("US queue processing complete!")

@app.function_name(name="TimerTriggerJP")
@app.timer_trigger(schedule="0 */20 * * * *", arg_name="timer")
def process_jp_queue(timer: func.TimerRequest):
    process_queue_messages(
        queue_name="amazonjp-queue",
        refinery_function=refineryJP,
        region_name="JP"
    )
    logging.info("JP queue processing complete!")