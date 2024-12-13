import streamlit as st
from util import data, viz
import pandas as pd

st.header("Data Insights")

st.subheader("Correlations")

timeseries_fx_rates = data.get_timeseries_data_fx()
timeseries_fx_rates.index = pd.to_datetime(timeseries_fx_rates.index)
timeseries_snapshots = data.get_collection_avg_price()
timeseries_snapshots.index = pd.to_datetime(timeseries_snapshots.index)


st.write("Currency Correlations")
st.dataframe(timeseries_fx_rates.corr("pearson"))

st.write("Avg Price Snapshot Correlations (Normalised)")
st.dataframe(data.get_normalised_baskets().corr())

with st.expander("Show Normalised Snapshot Prices"):
    st.dataframe(data.get_normalised_baskets())
st.subheader("Summary Statistics")
with st.expander("Top Items UK"):

    st.json(data.get_top_item_occ_counts_uk())
with st.expander("Top Items US"):
    st.json(data.get_top_item_occ_counts_us())

with st.expander("Top Items JP"):
    st.json(data.get_top_item_occ_counts_jp())
