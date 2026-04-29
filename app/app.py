import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import sys
import os

home_page = st.Page("app.py", title="Home", icon=None, default=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components.data_loader import load_rfm, SOURCES
from components.styles import apply_styles, sidebar_header, nav_bar, prev_next_nav
st.set_page_config(
    page_title="Retail Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("")

apply_styles()
sidebar_header("Home")
nav_bar("Home")

@st.cache_data(show_spinner=False)
def get_summary():
    total_customers = 0
    total_transactions = {
        "UCI Online Retail": 779425,
        "H&M Fashion":       28813419,
        "Instacart Grocery": 32434489,
    }
    at_risk   = 0
    champions = 0
    for source in SOURCES:
        df = load_rfm(source)
        total_customers += len(df)
        at_risk += len(df[df["cluster_label"].isin([
            "Lapsed", "At-Risk High Value", "At-Risk"
        ])])
        champions += len(df[df["cluster_label"].isin([
            "VIP Wholesale", "VIP Fashion", "Power Shoppers", "Champions"
        ])])
    return total_customers, sum(total_transactions.values()), at_risk, champions

total_customers, total_tx, at_risk, champions = get_summary()

st.markdown('<span class="chapter">Chapter 1 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# The Problem With Treating Every Customer the Same")

st.markdown("""
<div class="card" style="border-left: 3px solid #1B3A5C;">
<p style="font-size:1.05rem; line-height:1.8; color:#2C3E50; margin:0;">
Most retailers send the same promotions to every customer - the loyal buyer
who orders every week, the occasional browser who has not purchased in eight
months, and the high-value wholesale account who keeps the lights on.
The result? Wasted budget, irrelevant messages, and customers who disengage.
</p>
<p style="font-size:1.05rem; line-height:1.8; color:#2C3E50;
          margin-top:0.75rem; margin-bottom:0;">
This project asks a simple question:
<strong>what if we actually knew who each customer was?</strong>
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">The Scale of This Analysis</span>',
            unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-tile">
        <div class="kpi-value">{total_tx/1e6:.0f}M+</div>
        <div class="kpi-label">Transactions Analysed</div>
        <div class="kpi-sub">Across 3 retail verticals</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value">{total_customers/1e6:.2f}M</div>
        <div class="kpi-label">Unique Customers</div>
        <div class="kpi-sub">Gift, fashion and grocery</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value">{champions:,}</div>
        <div class="kpi-label">High-Value Customers</div>
        <div class="kpi-sub">Champions and VIP tiers</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value">{at_risk/total_customers*100:.0f}%</div>
        <div class="kpi-label">Customers at Risk</div>
        <div class="kpi-sub">Lapsed or going cold</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">How This Story Unfolds</span>',
            unsafe_allow_html=True)
st.markdown("### Six chapters. One clear answer.")

cols = st.columns(3)
chapters = [
    ("Data Overview",
     "Three real-world datasets. Over 62 million transactions cleaned, "
     "standardised, and made ready for analysis."),
    ("Segment Explorer",
     "Using RFM analysis and K-Means clustering, every customer is placed "
     "into one of four behaviour-based groups."),
    ("Marketing Targeting",
     "Each segment receives a tailored marketing strategy - the right "
     "message, channel, and priority for each customer type."),
]
for col, (title, desc) in zip(cols, chapters):
    with col:
        st.markdown(f"""
        <div class="card" style="height:100%;">
            <div style="font-family:'DM Serif Display',serif; font-size:1rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">{title}</div>
            <div style="font-size:0.85rem; color:#6B7A99;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

cols2 = st.columns(3)
chapters2 = [
    ("Churn Risk Report",
     "High-value customers showing signs of disengagement are flagged "
     "automatically - exported as a CSV ready for action."),
    ("Customer Lookup",
     "Enter any customer ID to retrieve their full profile, segment "
     "label, and a personalised recommendation."),
    ("The Takeaway",
     "Treating customers as individuals - not averages - is the "
     "difference between retention and churn."),
]
for col, (title, desc) in zip(cols2, chapters2):
    with col:
        st.markdown(f"""
        <div class="card" style="height:100%;">
            <div style="font-family:'DM Serif Display',serif; font-size:1rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">{title}</div>
            <div style="font-size:0.85rem; color:#6B7A99;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">The Methodology in Plain English</span>',
            unsafe_allow_html=True)

col_a, col_b = st.columns([1.2, 1])

with col_a:
    st.markdown("""
    <div class="card-mist">
        <div style="font-family:'DM Serif Display',serif; font-size:1.1rem;
                    color:#1B3A5C; margin-bottom:0.75rem;">
            RFM - Three questions about every customer
        </div>
        <div style="font-size:0.88rem; color:#2C3E50; line-height:1.8;">
            <strong>Recency</strong> - When did they last buy?
            A customer who bought yesterday is worth more than one who
            bought a year ago.<br><br>
            <strong>Frequency</strong> - How often do they buy?
            Regular buyers signal loyalty and trust.<br><br>
            <strong>Monetary</strong> - How much have they spent?
            Total spend reveals who drives revenue.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="card-mist">
        <div style="font-family:'DM Serif Display',serif; font-size:1.1rem;
                    color:#1B3A5C; margin-bottom:0.75rem;">
            K-Means - Letting the data decide the groups
        </div>
        <div style="font-size:0.88rem; color:#2C3E50; line-height:1.8;">
            Rather than manually defining customer tiers, K-Means
            clustering finds natural groupings in the data automatically
            - grouping customers who behave similarly together, without
            being told what the groups should look like in advance.
            <br><br>
            The result: four distinct, actionable customer tiers
            per retailer.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="insight">
    Use the navigation bar above to move between chapters.
    Start with <strong>Data Overview</strong> to understand what was built,
    or jump to <strong>Segment Explorer</strong> to see the results.
</div>
""", unsafe_allow_html=True)

prev_next_nav("Home")
