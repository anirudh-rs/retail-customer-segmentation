import pandas as pd
import numpy as np
import os
import streamlit as st

# ── Path resolution ───────────────────────────────────────────────────────────
def _get_processed_path():
    home = os.path.expanduser("~")
    candidate = os.path.join(home, "Retail Seg", "data", "processed")
    if os.path.isdir(candidate):
        return candidate
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        candidate = os.path.join(here, "data", "processed")
        if os.path.isdir(candidate):
            return os.path.abspath(candidate)
        here = os.path.dirname(here)
    return "/tmp/retail_data"

PROCESSED = _get_processed_path()

# ── Google Drive file IDs for large files ─────────────────────────────────────
DRIVE_IDS = {
    "hm_clean.parquet":          "1C-KP7dddCRY45XSXThG2xu1aqHVf1h8W",
    "inst_clean.parquet":        "1eEsiFykzk7pJs8ZHM_m-yAMtIu47B3Oq",
    "rfm_hm.parquet":            "1IZF9RfMcrqzElA9oHM_f9VJJ_PSks-QU",
    "rfm_hm_clustered.parquet":  "1NdTMwzMIn7p9WPYeSK7Rt2OyLWbRWuaC",
}

CACHE_DIR = "/tmp/retail_data"


def _get_file(filename):
    """
    Returns path to file. If not available locally, downloads from Google Drive.
    """
    local_path = os.path.join(PROCESSED, filename)
    if os.path.exists(local_path):
        return local_path

    # Fall back to Google Drive
    os.makedirs(CACHE_DIR, exist_ok=True)
    cached_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cached_path):
        return cached_path

    if filename not in DRIVE_IDS:
        raise FileNotFoundError(f"Cannot find {filename} locally or on Drive.")

    try:
        import gdown
        file_id = DRIVE_IDS[filename]
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Downloading {filename} from Google Drive...")
        gdown.download(url, cached_path, quiet=False)
        return cached_path
    except Exception as e:
        raise RuntimeError(f"Failed to download {filename}: {e}")


# ── Loaders ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data...")
def load_rfm(source):
    fname_map = {
        "UCI Online Retail": "rfm_uci_clustered.parquet",
        "H&M Fashion":       "rfm_hm_clustered.parquet",
        "Instacart Grocery": "rfm_inst_clustered.parquet",
    }
    return pd.read_parquet(_get_file(fname_map[source]))


@st.cache_data(show_spinner="Loading transactions...")
def load_transactions(source):
    fname_map = {
        "UCI Online Retail": "uci_clean.parquet",
        "H&M Fashion":       "hm_clean.parquet",
        "Instacart Grocery": "inst_clean.parquet",
    }
    df = pd.read_parquet(_get_file(fname_map[source]))
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


# ── Constants ─────────────────────────────────────────────────────────────────
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
    "UCI Online Retail": "\u00a3",
    "H&M Fashion":       "\u00a3",
    "Instacart Grocery": "items",
}