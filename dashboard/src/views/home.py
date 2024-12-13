import streamlit as st
from util import data, viz
import pandas as pd

st.header("Overview")
st.plotly_chart(viz.plot_min_values(data.get_normalised_baskets()))

st.subheader("Historical Data")
with st.expander("Show FX Timeseries"):
    timeseries_fx_rates = data.get_timeseries_data_fx()
    st.plotly_chart(
        viz.plot_timeseries_fx(timeseries_fx_rates["gbp_data"].to_frame(), "GBP")
    )
    st.plotly_chart(
        viz.plot_timeseries_fx(timeseries_fx_rates["usd_data"].to_frame(), "USD")
    )
    st.plotly_chart(
        viz.plot_timeseries_fx(timeseries_fx_rates["jpy_data"].to_frame(), "JPY")
    )

with st.expander("Show Snapshot Timeseries"):
    timeseries_snapshots = data.get_collection_avg_price()
    st.plotly_chart(
        viz.plot_timeseries_snapshot(
            timeseries_snapshots["us_data"].to_frame().sort_index(ascending=True),
            "USD",
            "US",
        )
    )
    st.plotly_chart(
        viz.plot_timeseries_snapshot(
            timeseries_snapshots["uk_data"].to_frame().sort_index(ascending=True),
            "GBP",
            "UK",
        )
    )
    st.plotly_chart(
        viz.plot_timeseries_snapshot(
            timeseries_snapshots["jp_data"].to_frame().sort_index(ascending=True),
            "JPY",
            "JP",
        )
    )
