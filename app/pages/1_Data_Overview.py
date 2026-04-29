import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from components.styles import apply_styles, sidebar_header, nav_bar, prev_next_nav
st.set_page_config(
    page_title="Data Overview - Retail Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
sidebar_header("Data Overview")
nav_bar("Data Overview")

st.markdown('<span class="chapter">Chapter 2 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# Where the Data Comes From")
st.markdown("""
<p style="font-size:1rem; color:#6B7A99; max-width:700px; line-height:1.7;
          margin-bottom:1.5rem;">
Three publicly available datasets, each from a different retail sector.
Together they represent over 62 million real transactions and 1.57 million
unique customers - cleaned, standardised, and ready for analysis.
</p>
""", unsafe_allow_html=True)

dataset_meta = [
    {
        "name":       "UCI Online Retail II",
        "sector":     "Gift and Homeware",
        "origin":     "UK-based online retailer",
        "period":     "Dec 2009 to Dec 2011",
        "rows_clean": "779,425",
        "customers":  "5,878",
        "dropped":    "27%",
        "note":       "The classic RFM benchmark dataset. Real invoices, real "
                      "customers, real returns. Messy enough to require serious "
                      "cleaning.",
        "color":      "#1B3A5C",
    },
    {
        "name":       "H&M Fashion Transactions",
        "sector":     "Fashion Retail",
        "origin":     "H&M Group via Kaggle competition",
        "period":     "Sep 2018 to Sep 2020",
        "rows_clean": "28,813,419",
        "customers":  "1,362,281",
        "dropped":    "9%",
        "note":       "Released by H&M for a recommendation challenge. Includes "
                      "customer demographics and rich article metadata.",
        "color":      "#C8873A",
    },
    {
        "name":       "Instacart Grocery Orders",
        "sector":     "Online Grocery",
        "origin":     "Instacart via Kaggle competition",
        "period":     "Reconstructed from order sequences",
        "rows_clean": "32,434,489",
        "customers":  "206,209",
        "dropped":    "0%",
        "note":       "3M+ grocery orders across 200k users. No prices - monetary "
                      "value is basket size. High-frequency purchasing makes "
                      "RFM patterns vivid.",
        "color":      "#2E7D6A",
    },
]

for meta in dataset_meta:
    st.markdown(f"""
    <div class="card" style="border-top: 3px solid {meta['color']};">
        <div style="display:flex; justify-content:space-between;
                    align-items:flex-start; flex-wrap:wrap; gap:1rem;">
            <div style="flex:2; min-width:280px;">
                <div style="font-family:'DM Serif Display',serif;
                            font-size:1.15rem; color:#1B3A5C;
                            margin-bottom:0.25rem;">{meta['name']}</div>
                <div style="font-size:0.78rem; color:#6B7A99;
                            margin-bottom:0.6rem;">
                    {meta['sector']} &nbsp;&middot;&nbsp; {meta['origin']}
                    &nbsp;&middot;&nbsp; {meta['period']}
                </div>
                <div style="font-size:0.87rem; color:#4A5568;
                            line-height:1.6;">{meta['note']}</div>
            </div>
            <div style="flex:1; min-width:220px; display:flex;
                        gap:1rem; flex-wrap:wrap;">
                <div style="text-align:center; padding:0.6rem 1rem;
                            background:#F7F9FC; border-radius:8px;
                            min-width:90px;">
                    <div style="font-family:'DM Serif Display',serif;
                                font-size:1.3rem;
                                color:{meta['color']};">{meta['customers']}</div>
                    <div style="font-size:0.68rem; color:#6B7A99;
                                text-transform:uppercase; letter-spacing:0.07em;
                                margin-top:0.2rem;">Customers</div>
                </div>
                <div style="text-align:center; padding:0.6rem 1rem;
                            background:#F7F9FC; border-radius:8px;
                            min-width:90px;">
                    <div style="font-family:'DM Serif Display',serif;
                                font-size:1.3rem;
                                color:{meta['color']};">{meta['rows_clean']}</div>
                    <div style="font-size:0.68rem; color:#6B7A99;
                                text-transform:uppercase; letter-spacing:0.07em;
                                margin-top:0.2rem;">Clean Rows</div>
                </div>
                <div style="text-align:center; padding:0.6rem 1rem;
                            background:#F7F9FC; border-radius:8px;
                            min-width:90px;">
                    <div style="font-family:'DM Serif Display',serif;
                                font-size:1.3rem;
                                color:{meta['color']};">{meta['dropped']}</div>
                    <div style="font-size:0.68rem; color:#6B7A99;
                                text-transform:uppercase; letter-spacing:0.07em;
                                margin-top:0.2rem;">Rows Dropped</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">What Cleaning Was Done</span>',
            unsafe_allow_html=True)
st.markdown("### Raw data is never ready. Here is what we fixed.")

cleaning_steps = [
    ("Removed anonymous transactions",
     "Any transaction without a customer ID was discarded. You cannot "
     "build a customer profile without knowing who the customer is."),
    ("Removed cancelled orders",
     "UCI invoices starting with C are cancellations - refunds, not "
     "purchases. Including them would understate revenue and distort "
     "recency."),
    ("Removed zero and negative values",
     "Rows with zero or negative quantity and price are data entry "
     "errors. Excluded from all calculations."),
    ("Removed duplicates",
     "26,000+ duplicate rows in UCI, 2.97 million in H&M. Exact "
     "duplicates were dropped, keeping the first occurrence."),
    ("Capped outliers at the 99th percentile",
     "A handful of wholesale accounts in UCI spent 100x the average "
     "customer. Capping at the 99th percentile prevents them from "
     "distorting cluster boundaries while keeping them in the dataset."),
]

for i, (title, desc) in enumerate(cleaning_steps):
    st.markdown(f"""
    <div style="display:flex; gap:1rem; margin-bottom:0.75rem;
                align-items:flex-start;">
        <div style="min-width:28px; height:28px; background:#1B3A5C;
                    border-radius:50%; display:flex; align-items:center;
                    justify-content:center; font-size:0.75rem; color:#fff;
                    font-weight:600; margin-top:0.1rem;">
            {i+1}
        </div>
        <div>
            <div style="font-weight:500; font-size:0.9rem;
                        color:#1A1F2E;">{title}</div>
            <div style="font-size:0.83rem; color:#6B7A99; margin-top:0.2rem;
                        line-height:1.6;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">The Common Schema</span>',
            unsafe_allow_html=True)
st.markdown("### All three datasets were mapped to the same structure.")
st.markdown("""
<p style="font-size:0.88rem; color:#6B7A99; max-width:650px; line-height:1.7;">
Despite coming from completely different retailers with different formats,
all three datasets were standardised to seven shared columns before any
analysis began. This allows the same RFM engine and clustering pipeline
to run on any of them identically.
</p>
""", unsafe_allow_html=True)

schema = {
    "customer_id":  "Unique identifier for each customer",
    "invoice_date": "Date of each transaction",
    "order_id":     "Unique identifier for each order or invoice",
    "revenue":      "Transaction value (GBP for UCI and H&M, basket size for Instacart)",
    "product_name": "Product description or article ID",
    "country":      "Customer country or retail origin label",
    "source":       "Which dataset this row came from",
}

rows = ""
for col, desc in schema.items():
    rows += f"""<tr>
        <td><code style='background:#EEF2F7; padding:2px 6px;
            border-radius:4px; font-size:0.8rem;'>{col}</code></td>
        <td>{desc}</td>
    </tr>"""

st.markdown(f"""
<table class='styled-table'>
    <thead><tr><th>Column</th><th>What it contains</th></tr></thead>
    <tbody>{rows}</tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight" style="margin-top:1.5rem;">
    Continue to <strong>Segment Explorer</strong> to see how these
    customers were grouped into behaviour-based segments using RFM
    scoring and K-Means clustering.
</div>
""", unsafe_allow_html=True)

prev_next_nav("Data Overview")
