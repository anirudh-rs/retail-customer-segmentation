import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from components.data_loader import load_rfm, SOURCES, CURRENCY_LABEL
from components.styles import apply_styles, sidebar_header, nav_bar, prev_next_nav

st.set_page_config(
    page_title="Churn Risk Report - Retail Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
sidebar_header("Churn Risk Report")
nav_bar("Churn Risk Report")

st.markdown('<span class="chapter">Chapter 5 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# Who Is About to Walk Out the Door?")
st.markdown("""
<p style="font-size:1rem; color:#6B7A99; max-width:700px; line-height:1.7;
          margin-bottom:1.5rem;">
Identifying a high-value customer who is quietly going cold is one of the
most commercially valuable things this analysis can do. The customers flagged
here were historically strong buyers - but their recency is now declining.
Act now, or lose them permanently.
</p>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    source = st.selectbox("Dataset", SOURCES, key="churn_source")
with col_b:
    recency_threshold = st.slider(
        "Flag customers inactive for more than (days)",
        min_value=30, max_value=365, value=90, step=10
    )
with col_c:
    min_monetary = st.slider(
        "Minimum historical spend to flag",
        min_value=0, max_value=5000, value=500, step=100
    )

df   = load_rfm(source)
curr = CURRENCY_LABEL[source]

at_risk = df[
    (df["recency"]  >  recency_threshold) &
    (df["monetary"] >= min_monetary) &
    (df["cluster_label"].isin([
        "Champions", "Loyal Regulars", "Casual Shoppers",
        "VIP Wholesale", "VIP Fashion", "Power Shoppers"
    ]))
].copy()

at_risk["risk_score"] = (
    (at_risk["recency"]  / at_risk["recency"].max()  * 50) +
    (at_risk["monetary"] / at_risk["monetary"].max() * 50)
).round(1)

at_risk = at_risk.sort_values("risk_score", ascending=False)

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

total_at_risk  = len(at_risk)
pct_base       = total_at_risk / len(df) * 100
avg_spend      = at_risk["monetary"].mean() if total_at_risk > 0 else 0
avg_recency    = at_risk["recency"].mean()  if total_at_risk > 0 else 0
potential_loss = at_risk["monetary"].sum()

curr_sym = "\u00a3" if curr != "items" else ""

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-tile">
        <div class="kpi-value" style="color:#C0392B;">{total_at_risk:,}</div>
        <div class="kpi-label">Customers Flagged</div>
        <div class="kpi-sub">{pct_base:.1f}% of customer base</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value">{avg_recency:.0f}d</div>
        <div class="kpi-label">Avg Days Inactive</div>
        <div class="kpi-sub">Since last purchase</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value">{curr_sym}{avg_spend:,.0f}</div>
        <div class="kpi-label">Avg Historical Spend</div>
        <div class="kpi-sub">Per flagged customer</div>
    </div>
    <div class="kpi-tile">
        <div class="kpi-value" style="color:#C0392B;">{curr_sym}{potential_loss:,.0f}</div>
        <div class="kpi-label">Revenue at Risk</div>
        <div class="kpi-sub">Combined spend of flagged customers</div>
    </div>
</div>
""", unsafe_allow_html=True)

if total_at_risk == 0:
    st.markdown("""
    <div class="card-mist" style="text-align:center; padding:2rem;">
        <div style="font-family:'DM Serif Display',serif; color:#2E7D6A;
                    font-size:1.1rem;">
            No customers flagged at these thresholds.
        </div>
        <div style="font-size:0.85rem; color:#6B7A99; margin-top:0.5rem;">
            Try lowering the recency threshold or minimum spend.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1])
    with col_l:
        st.markdown('<span class="chapter">Spend vs Inactivity</span>',
                    unsafe_allow_html=True)
        sample = at_risk.head(2000)
        fig = go.Figure(go.Scatter(
            x=sample["recency"],
            y=sample["monetary"],
            mode="markers",
            marker=dict(
                size=6,
                color=sample["risk_score"],
                colorscale=[[0, "#FEF3E2"], [0.5, "#C8873A"], [1, "#C0392B"]],
                showscale=True,
                colorbar=dict(title="Risk Score", thickness=12,
                              tickfont=dict(size=9, family="DM Sans")),
                opacity=0.7,
            ),
            text=sample["customer_id"],
            hovertemplate=(
                "<b>Customer:</b> %{text}<br>"
                "<b>Inactive:</b> %{x} days<br>"
                "<b>Spend:</b> %{y:,.0f}<br>"
                "<extra></extra>"
            ),
        ))
        fig.update_layout(
            xaxis=dict(title="Days Since Last Purchase",
                       tickfont=dict(size=10, family="DM Sans"),
                       gridcolor="#EEF2F7", zeroline=False),
            yaxis=dict(title="Total Spend",
                       tickfont=dict(size=10, family="DM Sans"),
                       gridcolor="#EEF2F7", zeroline=False),
            margin=dict(t=10, b=40, l=50, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})

    with col_r:
        st.markdown('<span class="chapter">By Segment</span>',
                    unsafe_allow_html=True)
        seg_breakdown = at_risk["cluster_label"].value_counts().reset_index()
        seg_breakdown.columns = ["Segment", "Count"]
        fig2 = go.Figure(go.Bar(
            x=seg_breakdown["Count"],
            y=seg_breakdown["Segment"],
            orientation="h",
            marker_color="#C0392B",
            opacity=0.8,
        ))
        fig2.update_layout(
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(size=9, family="DM Sans"),
                       gridcolor="#EEF2F7", zeroline=False),
            yaxis=dict(tickfont=dict(size=10, family="DM Sans"),
                       autorange="reversed"),
            height=340,
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig2, use_container_width=True,
                        config={"displayModeBar": False})

    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    st.markdown('<span class="chapter">Flagged Customers</span>',
                unsafe_allow_html=True)
    st.markdown("### Sorted by risk score - highest urgency first.")

    display_cols = {
        "customer_id":   "Customer ID",
        "cluster_label": "Segment",
        "recency":       "Days Inactive",
        "frequency":     "Total Orders",
        "monetary":      "Total Spend",
        "rfm_score":     "RFM Score",
        "risk_score":    "Risk Score",
    }

    display_df = (at_risk[list(display_cols.keys())]
                  .head(500)
                  .rename(columns=display_cols))
    display_df["Total Spend"] = display_df["Total Spend"].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=380,
        hide_index=True,
    )

    csv = (at_risk[list(display_cols.keys())]
           .rename(columns=display_cols)
           .to_csv(index=False))

    st.download_button(
        label=f"Download full report ({total_at_risk:,} customers)",
        data=csv,
        file_name=f"churn_risk_{source.lower().replace(' ', '_')}.csv",
        mime="text/csv",
    )

    st.markdown("""
    <div class="insight" style="margin-top:1rem;">
        <strong>What to do with this list:</strong> Pass the top-scoring
        rows directly to your CRM or email platform. Prioritise Champions
        and VIP customers first - their revenue impact is highest.
    </div>
    """, unsafe_allow_html=True)

prev_next_nav("Churn Risk Report")