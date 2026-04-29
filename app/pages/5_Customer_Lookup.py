import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from components.data_loader import (load_rfm, SOURCES, CLUSTER_LABELS,
                                    CURRENCY_LABEL, SEGMENT_COLORS)
from components.styles import (apply_styles, sidebar_header,
                                nav_bar, prev_next_nav)

st.set_page_config(
    page_title="Customer Lookup - Retail Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
sidebar_header("Customer Lookup")
nav_bar("Customer Lookup")

st.markdown('<span class="chapter">Chapter 6 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# Look Up Any Customer")
st.markdown("""
<p style="font-size:1rem; color:#6B7A99; max-width:700px; line-height:1.7;
          margin-bottom:1.5rem;">
Select a dataset, then either pick a random customer or choose from a
shuffled sample. The full profile loads instantly - no copy-pasting needed.
</p>
""", unsafe_allow_html=True)

recommendations = {
    "VIP Wholesale":     "Assign dedicated account management. Offer exclusive "
                         "early access to new lines and volume rebates. Do not "
                         "wait for them to disengage - proactive relationship "
                         "management is essential.",
    "VIP Fashion":       "Enrol in top loyalty tier if not already. Send curated "
                         "personalised communications - member-only previews, "
                         "styling picks, birthday rewards. Exclusivity, not "
                         "discounts.",
    "Power Shoppers":    "Introduce a subscription or standing order option to "
                         "lock in frequency. Personalised reorder reminders and "
                         "bundle deals on favourite categories.",
    "Champions":         "Nudge toward VIP tier - show them how close they are. "
                         "Double points event or milestone reward. Acknowledge "
                         "their loyalty explicitly.",
    "Loyal Regulars":    "Cross-sell into adjacent categories based on purchase "
                         "history. Post-purchase follow-up with relevant "
                         "recommendations 3 to 5 days after each order.",
    "Casual Shoppers":   "Re-engagement campaign at 45-day inactivity mark. "
                         "Seasonal or event-based messaging. Light-touch - one "
                         "campaign series maximum.",
    "Occasional Buyers": "Win-back offer with urgency at 90-day inactivity. "
                         "Time-limited discount or free delivery on next order. "
                         "Do not over-invest in paid channels for this tier.",
    "Lapsed":            "One win-back email maximum. If high historical spend: "
                         "meaningful offer. If low historical spend: suppress "
                         "from paid campaigns. Protect sender reputation.",
}

source = st.selectbox("Select dataset", SOURCES, key="lookup_source")
df     = load_rfm(source)
curr   = CURRENCY_LABEL[source]
labels = CLUSTER_LABELS[source]

if "lookup_seed" not in st.session_state:
    st.session_state.lookup_seed = 42
if "active_customer" not in st.session_state:
    st.session_state.active_customer = None
if "prev_source" not in st.session_state:
    st.session_state.prev_source = source

if st.session_state.prev_source != source:
    st.session_state.active_customer = None
    st.session_state.prev_source = source

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">Choose a Customer</span>',
            unsafe_allow_html=True)

sample_ids = (
    df["customer_id"]
    .sample(10, random_state=st.session_state.lookup_seed)
    .tolist()
)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Random Customer", use_container_width=True):
        st.session_state.active_customer = str(
            df["customer_id"].sample(1, random_state=None).iloc[0]
        )

with col2:
    options = ["Select from sample..."] + [str(i) for i in sample_ids]
    choice  = st.selectbox(
        "Sample of 10 customers",
        options=options,
        key=f"sample_drop_{st.session_state.lookup_seed}_{source}"
    )
    if choice != "Select from sample...":
        st.session_state.active_customer = choice

with col3:
    if st.button("Shuffle Sample", use_container_width=True):
        st.session_state.lookup_seed = int(np.random.randint(0, 99999))
        st.session_state.active_customer = None
        st.rerun()

if not st.session_state.active_customer:
    st.markdown("""
    <div class="card-mist" style="text-align:center; padding:2rem;
                                   margin-top:1rem;">
        <div style="font-size:0.9rem; color:#6B7A99;">
            Click <strong>Random Customer</strong> or select one from
            the sample dropdown above to see their full profile.
        </div>
    </div>
    """, unsafe_allow_html=True)
    prev_next_nav("Customer Lookup")
    st.stop()

customer_id = st.session_state.active_customer
match = df[df["customer_id"].astype(str) == customer_id]

if match.empty:
    st.markdown(f"""
    <div style="background:#FDF2F2; border-radius:10px;
                padding:1.25rem 1.5rem; border-left:3px solid #C0392B;
                margin-top:1rem;">
        <div style="color:#922B21; font-size:0.9rem;">
            Customer <strong>{customer_id}</strong> not found in
            {source}. Try shuffling the sample or picking a new
            random customer.
        </div>
    </div>
    """, unsafe_allow_html=True)
    prev_next_nav("Customer Lookup")
    st.stop()

row      = match.iloc[0]
segment  = row["cluster_label"]
meta     = labels.get(segment, {"badge": "badge-loyal"})
color    = SEGMENT_COLORS.get(segment, "#4A6FA5")
rec      = recommendations.get(segment, "No recommendation available.")
monetary = row["monetary"]
mon_disp = (f"\u00a3{monetary:,.2f}" if curr != "items"
            else f"{monetary:,.0f} items")

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card" style="border-top: 3px solid {color};">
    <div style="display:flex; align-items:center; gap:1rem;
                margin-bottom:1rem; flex-wrap:wrap;">
        <div>
            <div style="font-family:'DM Serif Display',serif; font-size:1.3rem;
                        color:#1B3A5C;">
                Customer {row['customer_id']}
            </div>
            <div style="margin-top:0.3rem;">
                <span class="badge {meta['badge']}">{segment}</span>
                <span style="font-size:0.78rem; color:#6B7A99;
                             margin-left:0.75rem;">{source}</span>
            </div>
        </div>
    </div>
    <div class="metric-row">
        <div class="metric-box">
            <div class="m-val">{row['recency']:.0f}d</div>
            <div class="m-lbl">Last Purchase</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{row['frequency']:.0f}</div>
            <div class="m-lbl">Total Orders</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{mon_disp}</div>
            <div class="m-lbl">Total Spend</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{row['r_score']}</div>
            <div class="m-lbl">Recency Score</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{row['f_score']}</div>
            <div class="m-lbl">Frequency Score</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{row['m_score']}</div>
            <div class="m-lbl">Monetary Score</div>
        </div>
        <div class="metric-box">
            <div class="m-val">{row['rfm_score']}/15</div>
            <div class="m-lbl">Overall RFM</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card" style="border-left: 3px solid {color};
                          margin-top:0.5rem;">
    <div style="font-family:'DM Serif Display',serif; font-size:1rem;
                color:#1B3A5C; margin-bottom:0.6rem;">
        Recommended Action
    </div>
    <div style="font-size:0.88rem; color:#4A5568;
                line-height:1.7;">{rec}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">RFM Score Breakdown</span>',
            unsafe_allow_html=True)

col_gauge, col_context = st.columns([1, 1.5])

with col_gauge:
    rfm_score = row["rfm_score"]
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rfm_score,
        number=dict(font=dict(size=36, family="DM Serif Display",
                              color="#1B3A5C")),
        gauge=dict(
            axis=dict(range=[3, 15],
                      tickfont=dict(size=9, family="DM Sans")),
            bar=dict(color=color, thickness=0.25),
            bgcolor="#F7F9FC",
            bordercolor="#DDE3EE",
            steps=[
                dict(range=[3,  6],  color="#FDF2F2"),
                dict(range=[6,  9],  color="#FEF9EE"),
                dict(range=[9,  12], color="#EDF7F4"),
                dict(range=[12, 15], color="#EBF2FB"),
            ],
            threshold=dict(
                line=dict(color=color, width=3),
                thickness=0.8,
                value=rfm_score
            ),
        ),
        title=dict(
            text="Overall RFM Score (3 to 15)",
            font=dict(size=11, family="DM Sans", color="#6B7A99")
        ),
    ))
    fig_gauge.update_layout(
        height=260,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, use_container_width=True,
                    config={"displayModeBar": False})

with col_context:
    score_bands = [
        (12, 15, "#1B4F8A", "Top tier",  "Champions and VIP customers"),
        (9,  12, "#2E7D6A", "Strong",    "Loyal, regular buyers"),
        (6,  9,  "#B45309", "Moderate",  "Occasional or lapsing customers"),
        (3,  6,  "#922B21", "Low",       "Dormant or lost customers"),
    ]
    st.markdown("<div style='padding-top:1rem;'>", unsafe_allow_html=True)
    for lo, hi, col_hex, label, desc in score_bands:
        active = lo <= rfm_score <= hi
        bg     = "#fff"      if active else "#F7F9FC"
        border = (f"2px solid {col_hex}" if active
                  else "1px solid #DDE3EE")
        marker = (
            f'<span style="margin-left:auto; font-size:0.75rem; '
            f'color:{col_hex}; font-weight:600;">this customer</span>'
            if active else ""
        )
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.75rem;
                    padding:0.6rem 0.9rem; background:{bg};
                    border:{border}; border-radius:8px;
                    margin-bottom:0.5rem;">
            <div style="width:10px; height:10px; border-radius:50%;
                        background:{col_hex}; flex-shrink:0;"></div>
            <div style="flex:1;">
                <span style="font-weight:500; font-size:0.85rem;
                             color:#1A1F2E;">
                    {lo} to {hi} &nbsp; {label}
                </span>
                <span style="font-size:0.78rem; color:#6B7A99;
                             margin-left:0.5rem;">{desc}</span>
            </div>
            {marker}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

prev_next_nav("Customer Lookup")
