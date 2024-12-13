from pymongo import MongoClient
from datetime import datetime
from custom_utils import InvalidConnection
import logging

class AzureCosmosDbClient:
    def __init__(self):
        self._account_client = None
        self._db_client = None
        self.client = None

    def initialize(self, connection_string: str, db_name: str, bucket: str) -> None:
        """Initialize the Cosmos DB client with connection parameters.
        
        Args:
            connection_string: MongoDB connection string
            db_name: Name of the database
            bucket: Name of the collection
            
        Raises:
            InvalidConnection: If any connection parameters are invalid
        """
        try:
            self._account_client = MongoClient(connection_string)
        except Exception as err:
            logging.error("Invalid Connection String! Couldn't create Cosmos Client")
            raise InvalidConnection(
                "Invalid connection string, could not create Cosmos client"
            ) from err

        try:
            self._db_client = self._account_client[db_name]
        except Exception as err:
            logging.error("Invalid Database Name! Couldn't connect")
            raise InvalidConnection("Invalid database name, could not create client") from err

        try:
            self.client = self._db_client[bucket]
        except Exception as err:
            logging.error("Invalid collection name! Couldn't connect")
            raise InvalidConnection("Invalid collection name, could not create client") from err

    def publish_processed_data(self, msg_artifact) -> None:
        """Publish processed data to Cosmos DB.
        
        Args:
            msg_artifact: Dictionary containing source, timestamp and processed data
            
        Raises:
            Exception: If there's an error publishing the data
        """
        try:
            
            if not all(key in msg_artifact for key in ['source', 'timestamp']):
                raise ValueError("Missing required fields in msg_artifact")
            
            document = {
                "source": msg_artifact['source'],
                "timestamp": msg_artifact['timestamp'],
                "collection": msg_artifact['collection'],

            }
            logging.info("Making Document")
            logging.info(f"{document}")
            response = self.client.insert_one(document)
            logging.info(f"New entry created with ID: {response.inserted_id}")
            
            # Log summary of inserted data
            logging.debug(f"Inserted {len(document['collection'])} records from source: {document['source']}")
            
        except Exception as e:
            logging.error(f"Error publishing data: {str(e)}")
            raise Exception(f"Failed to publish data: {str(e)}") from e