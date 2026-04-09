import pandas as pd
import numpy as np
import os
import streamlit as st
from huggingface_hub import hf_hub_download

REPO_ID   = "anirudh-rs/retail-segmentation-data"
CACHE_DIR = "/tmp/retail_data"

def _download(filename):
    return hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type="dataset",
        cache_dir=CACHE_DIR,
    )

@st.cache_data(show_spinner="Loading data...")
def load_rfm(source):
    fname_map = {
        "UCI Online Retail": "rfm_uci_clustered.parquet",
        "H&M Fashion":       "rfm_hm_clustered.parquet",
        "Instacart Grocery": "rfm_inst_clustered.parquet",
    }
    return pd.read_parquet(_download(fname_map[source]))

@st.cache_data(show_spinner="Loading transactions...")
def load_transactions(source):
    fname_map = {
        "UCI Online Retail": "uci_clean.parquet",
        "H&M Fashion":       "hm_clean.parquet",
        "Instacart Grocery": "inst_clean.parquet",
    }
    df = pd.read_parquet(_download(fname_map[source]))
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    return df

@st.cache_data(show_spinner=False)
def load_all_rfm():
    dfs = []
    for source in SOURCES:
        df = load_rfm(source)
        df["source"] = source
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

SOURCES = ["UCI Online Retail", "H&M Fashion", "Instacart Grocery"]

CLUSTER_LABELS = {
    "UCI Online Retail": {
        "VIP Wholesale":  {"icon": "Diamond", "badge": "badge-vip"},
        "Champions":      {"icon": "Trophy",  "badge": "badge-champ"},
        "Loyal Regulars": {"icon": "Cycle",   "badge": "badge-loyal"},
        "Lapsed":         {"icon": "Sleep",   "badge": "badge-lapsed"},
    },
    "H&M Fashion": {
        "VIP Fashion":     {"icon": "Diamond", "badge": "badge-vip"},
        "Champions":       {"icon": "Trophy",  "badge": "badge-champ"},
        "Casual Shoppers": {"icon": "Cycle",   "badge": "badge-loyal"},
        "Lapsed":          {"icon": "Sleep",   "badge": "badge-lapsed"},
    },
    "Instacart Grocery": {
        "Power Shoppers":    {"icon": "Diamond", "badge": "badge-vip"},
        "Loyal Regulars":    {"icon": "Trophy",  "badge": "badge-champ"},
        "Occasional Buyers": {"icon": "Cycle",   "badge": "badge-loyal"},
        "Lapsed":            {"icon": "Sleep",   "badge": "badge-lapsed"},
    },
}

SEGMENT_COLORS = {
    "VIP Wholesale":     "#C8873A",
    "VIP Fashion":       "#C8873A",
    "Power Shoppers":    "#C8873A",
    "Champions":         "#2E7D6A",
    "Loyal Regulars":    "#1B3A5C",
    "Casual Shoppers":   "#1B3A5C",
    "Occasional Buyers": "#7B68BE",
    "Lapsed":            "#C0392B",
}

CURRENCY_LABEL = {
    "UCI Online Retail": "GBP",
    "H&M Fashion":       "GBP",
    "Instacart Grocery": "items",
}