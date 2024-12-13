from custom_utils import InvalidConnection
from azure.storage.blob import BlobClient
import logging

class AzureBlobStorageClient:
    def __init__(self, connection_string: str, block_name:str, container_name:str="unprocdatastore"):
        try:
            self.blob_client = BlobClient.from_connection_string(connection_string, container_name, block_name)
        except Exception as err:
            logging.error("Invalid Connection String, container or blob name!, Couldn't create blob Client")
            raise InvalidConnection(
                "Invalid connection string, could not create blob client"
            )
    
    def get_data_from_blob(self,encoding:str='utf-8'):
        try:
            logging.info("attempting data fetch from blob")
            blob_content = self.blob_client.download_blob().readall()
            return blob_content.decode('utf-8')
        except Exception as e:
            print(f"Error reading blob: {e}")
            return None
