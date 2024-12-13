import numpy as np
import pandas as pd
from datetime import datetime
from util import data as dta
import streamlit as st
import json
from collections import Counter


@st.cache_data
def get_timeseries_data_fx():
    data = dta.get_all_api_data()
    gbp_data = {}
    jpy_data = {}
    usd_data = {}
    for entry in data:
        gbp_data[
            datetime.fromtimestamp(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        ] = entry["data"]["rates"]["GBP"]
        jpy_data[
            datetime.fromtimestamp(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        ] = entry["data"]["rates"]["JPY"]
        usd_data[
            datetime.fromtimestamp(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        ] = entry["data"]["rates"]["USD"]

    return pd.DataFrame(
        {"gbp_data": gbp_data, "jpy_data": jpy_data, "usd_data": usd_data}
    )


@st.cache_data
def process_raw_snapshot_all():
    raw_data = dta.get_all_snapshot_data()
    for entry in raw_data:
        entry["collection"] = json.loads(entry["collection"])
        entry["timestamp"] = datetime.fromtimestamp(entry["timestamp"] / 1000).strftime(
            "%Y-%m-%d %H:%M"
        )

    return raw_data


def get_timeseries_snapshot_uk():
    data = process_raw_snapshot_all()
    data = filter(lambda entry: "uk" in entry["source"], data)
    return list(data)


def get_timeseries_snapshot_jp():
    data = process_raw_snapshot_all()
    data = filter(lambda entry: "jp" in entry["source"], data)
    return list(data)


def get_timeseries_snapshot_us():
    data = process_raw_snapshot_all()
    data = filter(lambda entry: "us" in entry["source"], data)
    return list(data)


def _get_collection_avg(coll_code, catagory="price"):
    match coll_code:
        case "UK":
            data = get_timeseries_snapshot_uk()
        case "US":
            data = get_timeseries_snapshot_us()

        case "JP":
            data = get_timeseries_snapshot_jp()

    means = {}
    for entry in data:
        try:
            means[entry["timestamp"]] = np.round(
                np.mean([x[catagory] for x in entry["collection"]]), 2
            )
        except:
            means[entry["timestamp"]] = np.nan
    return means


def _get_collection_counts(coll_code, catagory="title"):
    match coll_code:
        case "UK":
            data = get_timeseries_snapshot_uk()
        case "US":
            data = get_timeseries_snapshot_us()

        case "JP":
            data = get_timeseries_snapshot_jp()

    counts = Counter()
    for entry in data:
        try:
            counts.update([x[catagory] for x in entry["collection"]])
        except:
            continue

    return counts


def get_collection_avg_price():
    us_data = _get_collection_avg("US")
    jp_data = _get_collection_avg("JP")
    uk_data = _get_collection_avg("UK")
    return (
        pd.DataFrame(
            {
                "jp_data": jp_data,
                "us_data": us_data,
                "uk_data": uk_data,
            }
        )
        .ffill()
        .bfill()
    )


def get_top_item_occ_counts_uk():
    uk_data = _get_collection_counts("UK")
    return uk_data.most_common(3)


def get_top_item_occ_counts_us():
    us_data = _get_collection_counts("US")
    return us_data.most_common(3)


def get_top_item_occ_counts_jp():
    jp_data = _get_collection_counts("JP")
    return jp_data.most_common(3)


def get_normalised_baskets():
    timeseries_fx_rates = get_timeseries_data_fx()
    timeseries_fx_rates.index = pd.to_datetime(timeseries_fx_rates.index)
    timeseries_snapshots = get_collection_avg_price()
    timeseries_snapshots.index = pd.to_datetime(timeseries_snapshots.index)
    timeseries_snapshots = timeseries_snapshots.resample("H").mean()
    timeseries_fx_rates = timeseries_fx_rates.resample("H").mean()
    df = timeseries_snapshots.join(timeseries_fx_rates, how="inner")
    df["jp_data"] = df["jp_data"] / df["jpy_data"]
    df.drop(columns={"jpy_data"}, inplace=True)
    df["us_data"] = df["us_data"] / df["usd_data"]
    df.drop(columns={"usd_data"}, inplace=True)
    df["uk_data"] = df["uk_data"] / df["gbp_data"]
    df.drop(columns={"gbp_data"}, inplace=True)

    return df
