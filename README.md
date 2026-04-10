# Retail Customer Segmentation & Targeting

A machine learning project that segments retail customers into distinct groups based on purchasing behaviour, then recommends personalised marketing strategies for each segment.

**Live demo:** https://retail-customer-segmentation.streamlit.app

---

## Overview

Most retailers treat every customer the same - the same promotions, the same emails, the same offers. This project uses RFM analysis and K-Means clustering across three real-world retail datasets to identify distinct customer behaviour tiers and translate them into actionable marketing strategies.

---

## Datasets

| Dataset | Sector | Customers | Transactions | Period |
|---|---|---|---|---|
| UCI Online Retail II | Gift and Homeware | 5,878 | 779,425 | 2009 - 2011 |
| H&M Fashion Transactions | Fashion Retail | 1,362,281 | 28,813,419 | 2018 - 2020 |
| Instacart Grocery Orders | Online Grocery | 206,209 | 32,434,489 | Reconstructed |

**Total: 62M+ transactions across 1.57M customers**

---

## Methodology

**RFM Scoring**
Every customer is scored on three dimensions - Recency (days since last purchase), Frequency (number of orders), and Monetary value (total spend). Scores are ranked 1-5 using quintiles and combined into an overall RFM rating.

**Clustering**
K-Means clustering groups customers with similar RFM profiles together. The optimal number of clusters was selected using elbow curve analysis - k=4 was chosen over the silhouette-optimal k=2 because four clusters produce meaningfully distinct, actionable segments.

**Outlier Handling**
Values were capped at the 99th percentile before clustering to prevent wholesale accounts from distorting cluster boundaries.

**Segments**
The same four-tier structure emerged independently across all three datasets:

| Tier | Description |
|---|---|
| VIP / Power Shoppers | Recent, frequent, highest spend - protect at all costs |
| Champions | Strong across all dimensions - nudge toward VIP |
| Loyal Regulars / Casual Shoppers | Reliable middle tier - upsell and cross-sell |
| Lapsed | Gone quiet - selective win-back only |

---

## Dashboard

Built with Streamlit, the dashboard has six pages:

- **Home** - project overview and headline numbers
- **Data Overview** - datasets, cleaning steps, and common schema
- **Segment Explorer** - interactive cluster profiles per dataset
- **Marketing Targeting** - recommended strategy per segment
- **Churn Risk Report** - flags high-value customers going cold, exportable as CSV
- **Customer Lookup** - instant RFM profile for any customer ID with random and sample selection

---

## Tech Stack

- Python, pandas, numpy
- scikit-learn (K-Means, StandardScaler, PCA, silhouette scoring)
- Plotly, Seaborn
- Streamlit
- Yellowbrick (elbow method)
- Google Drive + gdown (large file storage)

---

## Project Structure

```
retail-customer-segmentation/
├── app/
│   ├── app.py                          # Streamlit entry point
│   ├── components/
│   │   ├── data_loader.py              # Loads parquet files locally or from Drive
│   │   └── styles.py                   # Shared CSS and navigation components
│   └── pages/
│       ├── 1_Data_Overview.py
│       ├── 2_Segment_Explorer.py
│       ├── 3_Marketing_Targeting.py
│       ├── 4_Churn_Report.py
│       └── 5_Customer_Lookup.py
├── notebooks/
│   ├── exploration.ipynb               # EDA and data inspection
│   ├── rfm_scoring.ipynb               # RFM feature engineering
│   └── clustering.ipynb                # K-Means modelling and profiling
├── data/
│   └── processed/                      # Small parquet files tracked in repo
├── outputs/                            # Saved charts and reports
└── requirements.txt
```

---

## Running Locally

```bash
git clone https://github.com/anirudh-rs/retail-customer-segmentation.git
cd retail-customer-segmentation
conda create -n retail_seg python=3.11 -y
conda activate retail_seg
pip install -r app/requirements.txt
cd app
streamlit run app.py
```

The app loads small parquet files from the repo directly. The two large files (H&M and Instacart transactions) are fetched from Google Drive automatically on first run via gdown.

---

## Data Sources

- [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) - UCI Machine Learning Repository
- [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations) - Kaggle
- [Instacart Market Basket Analysis](https://www.kaggle.com/competitions/instacart-market-basket-analysis) - Kaggle
