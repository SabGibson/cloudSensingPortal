import pymongo
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

DB_NAME = "IOTDB"
CONNECTION_STRING = os.environ.get("AZURE_CONNECTION_STRING")
AZURE_COLLECTION_STRING_ONE = os.environ.get("AZURE_COLLECTION_STRING_ONE")
AZURE_COLLECTION_STRING_TWO = os.environ.get("AZURE_COLLECTION_STRING_TWO")
client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DB_NAME]
snapshot_collection = db["snapshots"]
fxgoldencopydata_collection = db["fxgoldencopy"]
