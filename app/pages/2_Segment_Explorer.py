import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from components.data_loader import (load_rfm, SOURCES, CLUSTER_LABELS,
                                    SEGMENT_COLORS, CURRENCY_LABEL)
from components.styles import apply_styles, sidebar_header, nav_bar, prev_next_nav

st.set_page_config(
    page_title="Segment Explorer - Retail Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
sidebar_header("Segment Explorer")
nav_bar("Segment Explorer")

st.markdown('<span class="chapter">Chapter 3 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# Who Are Your Customers, Really?")
st.markdown("""
<p style="font-size:1rem; color:#6B7A99; max-width:700px; line-height:1.7;
          margin-bottom:1.5rem;">
Every customer was scored on three dimensions - Recency, Frequency, and
Monetary value - then grouped by K-Means clustering into four natural
behaviour tiers. Select a dataset below to explore its segments.
</p>
""", unsafe_allow_html=True)

source = st.selectbox("Select retail dataset", SOURCES, key="seg_source")
df     = load_rfm(source)
curr   = CURRENCY_LABEL[source]
labels = CLUSTER_LABELS[source]

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">The Four Tiers</span>',
            unsafe_allow_html=True)

seg_counts = df["cluster_label"].value_counts()
tier_order = list(labels.keys())

cols = st.columns(4)
for col, tier in zip(cols, tier_order):
    count = seg_counts.get(tier, 0)
    pct   = count / len(df) * 100
    meta  = labels[tier]
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:1.25rem 1rem;">
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">{tier}</div>
            <div style="font-family:'DM Serif Display',serif; font-size:1.8rem;
                        color:#1B3A5C; line-height:1;">{count:,}</div>
            <div style="font-size:0.72rem; color:#6B7A99; text-transform:uppercase;
                        letter-spacing:0.07em; margin-top:0.2rem;">
                {pct:.1f}% of customers
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1.3])

with col_l:
    st.markdown('<span class="chapter">Customer Distribution</span>',
                unsafe_allow_html=True)
    colors = [SEGMENT_COLORS.get(t, "#4A6FA5") for t in tier_order]
    counts = [seg_counts.get(t, 0) for t in tier_order]
    fig_pie = go.Figure(go.Pie(
        labels=tier_order,
        values=counts,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="percent",
        textfont=dict(size=12, family="DM Sans"),
        hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>"
                      "%{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(font=dict(size=11, family="DM Sans"), orientation="h",
                    yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        height=320,
        annotations=[dict(
            text=f"<b>{len(df):,}</b>",
            x=0.5, y=0.5,
            font=dict(size=13, family="DM Serif Display"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True,
                    config={"displayModeBar": False})

with col_r:
    st.markdown('<span class="chapter">RFM Profile by Segment</span>',
                unsafe_allow_html=True)
    profile = df.groupby("cluster_label").agg(
        Recency   = ("recency",   "mean"),
        Frequency = ("frequency", "mean"),
        Monetary  = ("monetary",  "mean"),
    ).round(1).reindex(tier_order)
    fig_bar = go.Figure()
    for metric, color in zip(
        ["Recency", "Frequency", "Monetary"],
        ["#1B3A5C", "#C8873A", "#2E7D6A"]
    ):
        fig_bar.add_trace(go.Bar(
            name=metric,
            x=profile.index,
            y=profile[metric],
            marker_color=color,
            opacity=0.85,
        ))
    fig_bar.update_layout(
        barmode="group",
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(size=11, family="DM Sans"), orientation="h",
                    yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        xaxis=dict(tickfont=dict(size=10, family="DM Sans"),
                   showgrid=False, zeroline=False),
        yaxis=dict(tickfont=dict(size=10, family="DM Sans"),
                   gridcolor="#EEF2F7", zeroline=False),
        height=320,
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_bar, use_container_width=True,
                    config={"displayModeBar": False})

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
st.markdown('<span class="chapter">Segment Deep Dive</span>',
            unsafe_allow_html=True)
st.markdown("### What does each tier actually look like?")

seg_detail = df.groupby("cluster_label").agg(
    customers   = ("customer_id", "count"),
    avg_recency = ("recency",     "mean"),
    avg_freq    = ("frequency",   "mean"),
    avg_mon     = ("monetary",    "mean"),
    avg_score   = ("rfm_score",   "mean"),
).round(1).reindex(tier_order)

segment_descriptions = {
    "VIP Wholesale":     "Bought recently, bought often, spent the most. "
                         "These are your most valuable accounts - protect them "
                         "at all costs.",
    "VIP Fashion":       "High engagement, high spend, highly recent. "
                         "Your most loyal fashion advocates. Reward and retain.",
    "Power Shoppers":    "Order constantly and fill large baskets. "
                         "The backbone of grocery revenue. High retention priority.",
    "Champions":         "Strong across all three dimensions. Active, frequent, "
                         "and valuable. Close to VIP - nudge them over the line.",
    "Loyal Regulars":    "Consistent buyers with moderate spend. "
                         "Reliable revenue. Upsell and cross-sell opportunities.",
    "Casual Shoppers":   "Moderate recency and low frequency. Engaged but not "
                         "committed. Targeted promotions could convert them.",
    "Occasional Buyers": "Buy infrequently but are not lost yet. "
                         "A well-timed offer could re-engage them.",
    "Lapsed":            "Have not bought in a long time. Win-back campaigns "
                         "are the only lever here.",
}

for tier in tier_order:
    if tier not in seg_detail.index:
        continue
    row      = seg_detail.loc[tier]
    meta     = labels[tier]
    desc     = segment_descriptions.get(tier, "")
    pct      = row["customers"] / len(df) * 100
    avg_mon  = row["avg_mon"]
    mon_label = (f"\u00a3{avg_mon:,.0f}"
                 if curr != "items" else f"{avg_mon:,.0f} items")

    st.markdown(f"""
    <div class="card" style="margin-bottom:0.75rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;
                    margin-bottom:0.75rem;">
            <span style="font-family:'DM Serif Display',serif;
                         font-size:1.05rem; color:#1B3A5C;">{tier}</span>
            <span class="badge {meta['badge']}">
                {row['customers']:,.0f} customers &middot; {pct:.1f}%
            </span>
        </div>
        <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                  margin-bottom:0.75rem;">{desc}</p>
        <div class="metric-row">
            <div class="metric-box">
                <div class="m-val">{row['avg_recency']:.0f}d</div>
                <div class="m-lbl">Avg Recency</div>
            </div>
            <div class="metric-box">
                <div class="m-val">{row['avg_freq']:.1f}</div>
                <div class="m-lbl">Avg Orders</div>
            </div>
            <div class="metric-box">
                <div class="m-val">{mon_label}</div>
                <div class="m-lbl">Avg Spend</div>
            </div>
            <div class="metric-box">
                <div class="m-val">{row['avg_score']:.1f}/15</div>
                <div class="m-lbl">RFM Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="insight">
    Now that you know who is in each segment, head to
    <strong>Marketing Targeting</strong> to see what to do about it.
</div>
""", unsafe_allow_html=True)

prev_next_nav("Segment Explorer")