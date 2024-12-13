from mongoclient import  AzureCosmosDbClient
from azureblobdbclient import AzureBlobStorageClient
from amazonukrefinery import process_amazonuk_html
from amazonusrefinery import process_amazonus_html
from amazonjprefinery import process_amazonjp_html
import logging
import json
import os

def refineryUK(message):
    msg_artifact = json.loads(message)
    try:
        blob_client = AzureBlobStorageClient(os.environ['STORAGE_CONNECT_STRING'],msg_artifact["blobName"])
    except Exception as e:
        logging.error(f"error setting up blob connection {e}")
        raise Exception
    
    try:
        db_client = AzureCosmosDbClient()
        db_client.initialize(os.environ['DB_CONNECT_STRING'],"IOTDB","snapshots")
    except Exception as e:
        logging.error(f"error setting up db connection {e}")
        raise Exception
    
    logging.info("setup data clients")
    logging.info("fetching raw data")
    try:
        raw_data = blob_client.get_data_from_blob()
    except Exception as e:
        logging.error(f"{e}")
        raise Exception
    logging.info("fetched raw data")
    
    if raw_data:
        logging.info("processing raw data ...")
        processed_data = process_amazonuk_html(raw_data)
        logging.info("processing raw data ... complete!")
        

        document = {
        "source":msg_artifact["source"],
        "timestamp":msg_artifact["timestamp"],
        "collection":processed_data
        }

        db_client.publish_processed_data(document)
        logging.info("returning")
    else:
        logging.info("no data from blob")

def refineryUS(message):
    msg_artifact = json.loads(message)
    try:
        blob_client = AzureBlobStorageClient(os.environ['STORAGE_CONNECT_STRING'],msg_artifact["blobName"])
    except Exception as e:
        logging.error(f"error setting up blob connection {e}")
        raise Exception
    
    try:
        db_client = AzureCosmosDbClient()
        db_client.initialize(os.environ['DB_CONNECT_STRING'],"IOTDB","snapshots")
    except Exception as e:
        logging.error(f"error setting up db connection {e}")
        raise Exception
    
    logging.info("setup data clients")
    logging.info("fetching raw data")
    try:
        raw_data = blob_client.get_data_from_blob()
    except Exception as e:
        logging.error(f"{e}")
        raise Exception
    logging.info("fetched raw data")
 
    if raw_data:
        logging.info("processing raw data ...")
        processed_data = process_amazonus_html(raw_data)
        
        logging.info("processing raw data ... complete!")
        document = {
        "source":msg_artifact["source"],
        "timestamp":msg_artifact["timestamp"],
        "collection":processed_data
        }
        db_client.publish_processed_data(document)
        logging.info("returning")
    else:
        logging.info("no data from blob")

def refineryJP(message):
    msg_artifact = json.loads(message)
    try:
        blob_client = AzureBlobStorageClient(os.environ['STORAGE_CONNECT_STRING'],msg_artifact["blobName"])
    except Exception as e:
        logging.error(f"error setting up blob connection {e}")
        raise Exception
    
    try:
        db_client = AzureCosmosDbClient()
        db_client.initialize(os.environ['DB_CONNECT_STRING'],"IOTDB","snapshots")
    except Exception as e:
        logging.error(f"error setting up db connection {e}")
        raise Exception
    
    logging.info("setup data clients")
    logging.info("fetching raw data")
    try:
        raw_data = blob_client.get_data_from_blob()
    except Exception as e:
        logging.error(f"{e}")
        raise Exception
    logging.info("fetched raw data")
    
    if raw_data:
        logging.info("processing raw data ...")
        processed_data = process_amazonjp_html(raw_data)
        
        logging.info("processing raw data ... complete!")
        document = {
        "source":msg_artifact["source"],
        "timestamp":msg_artifact["timestamp"],
        "collection":processed_data
        }
        db_client.publish_processed_data(document)
        logging.info("returning")
    else:
        logging.info("no data from blob")

    