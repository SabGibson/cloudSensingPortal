import streamlit as st
from util.data import *

st.header("Mined Data Viewer")

with st.expander("Show Amazon UK Snapshots in DB"):
    st.json(get_all_snapshot_uk_data())

with st.expander("Show Amazon US Snapshots in DB"):
    st.json(get_all_snapshot_us_data())

with st.expander("Show Amazon JP Snapshots in DB"):
    st.json(get_all_snapshot_jp_data())

with st.expander("Show all Snapshots in DB"):
    st.json(get_all_snapshot_data())
