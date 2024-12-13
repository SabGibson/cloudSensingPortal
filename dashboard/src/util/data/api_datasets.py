import streamlit as st
from util import client


# @st.cache_data
def get_all_api_data():
    cursor = client.fxgoldencopydata_collection.find()
    return [*cursor]
