from util import client
import streamlit as st


@st.cache_data
def get_all_snapshot_data():
    cursor = client.snapshot_collection.find()
    return [*cursor]


@st.cache_data
def get_all_snapshot_uk_data():
    cursor = client.snapshot_collection.find({"source": "amazonuk-queue"})
    return [*cursor]


@st.cache_data
def get_all_snapshot_us_data():
    cursor = client.snapshot_collection.find({"source": "amazonus-queue"})
    return [*cursor]


@st.cache_data
def get_all_snapshot_jp_data():
    cursor = client.snapshot_collection.find({"source": "amazonjp-queue"})
    return [*cursor]
