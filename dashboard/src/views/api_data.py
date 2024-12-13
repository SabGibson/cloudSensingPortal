import streamlit as st
from util.data import *

st.header("API Data Viewer")

with st.expander("Show API Data in DB"):
    st.json(get_all_api_data())
