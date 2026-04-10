import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from components.data_loader import load_rfm, SOURCES, CLUSTER_LABELS, CURRENCY_LABEL
from components.styles import apply_styles, sidebar_header, nav_bar, prev_next_nav
st.set_page_config(
    page_title="Marketing Targeting - Retail Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
sidebar_header("Marketing Targeting")
nav_bar("Marketing Targeting")

st.markdown('<span class="chapter">Chapter 4 of 6</span>',
            unsafe_allow_html=True)
st.markdown("# From Insight to Action")
st.markdown("""
<p style="font-size:1rem; color:#6B7A99; max-width:700px; line-height:1.7;
          margin-bottom:1.5rem;">
Knowing which segment a customer belongs to is only half the job.
The other half is knowing exactly what to do about it. Select a dataset
and a segment to see the recommended marketing strategy.
</p>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    source = st.selectbox("Retail dataset", SOURCES, key="tgt_source")
with col_b:
    segments = list(CLUSTER_LABELS[source].keys())
    segment  = st.selectbox("Customer segment", segments, key="tgt_seg")

df     = load_rfm(source)
labels = CLUSTER_LABELS[source]
curr   = CURRENCY_LABEL[source]

strategies = {
    "VIP Wholesale": {
        "priority": "CRITICAL", "priority_color": "#C8873A",
        "goal":    "Protect and deepen the relationship",
        "action":  "Dedicated account management and exclusive early access",
        "channel": "Direct outreach - phone, email, account manager",
        "message": "Appreciative and exclusive. These customers know their "
                   "value. Skip the discounts - offer access, priority, "
                   "and recognition instead.",
        "offer":   "Early access to new product lines, volume loyalty "
                   "rebates, dedicated support contact",
        "timing":  "Proactive - do not wait for signs of disengagement",
        "kpi":     "Retention rate, revenue per account, order frequency",
        "risk":    "Losing even one VIP account has outsized revenue impact. "
                   "Monitor engagement weekly.",
    },
    "VIP Fashion": {
        "priority": "CRITICAL", "priority_color": "#C8873A",
        "goal":    "Sustain loyalty and grow basket size",
        "action":  "Exclusive loyalty programme and personal styling perks",
        "channel": "App push notifications, personalised email, loyalty app",
        "message": "Make them feel like insiders. First access, curated "
                   "picks, member-only events. They respond to exclusivity, "
                   "not discounts.",
        "offer":   "Early sale access, styling recommendations, birthday "
                   "rewards, free returns on all orders",
        "timing":  "Ongoing - maintain a regular but not overwhelming cadence",
        "kpi":     "Retention rate, average order value, loyalty tier "
                   "progression",
        "risk":    "Over-communicating can fatigue even your best customers. "
                   "Quality over quantity.",
    },
    "Power Shoppers": {
        "priority": "CRITICAL", "priority_color": "#C8873A",
        "goal":    "Maintain frequency and grow basket size",
        "action":  "Loyalty rewards programme and personalised reorder "
                   "reminders",
        "channel": "App notifications, email, in-app personalisation",
        "message": "Convenience and value. Remind them of items they buy "
                   "regularly and offer bundle deals on favourite categories.",
        "offer":   "Points per order, free delivery threshold, subscription "
                   "option, personalised your usuals feature",
        "timing":  "Weekly touchpoints aligned to typical order cadence",
        "kpi":     "Order frequency, basket size, subscription conversion rate",
        "risk":    "Any friction in the ordering experience will drive them "
                   "to a competitor.",
    },
    "Champions": {
        "priority": "HIGH", "priority_color": "#2E7D6A",
        "goal":    "Convert to VIP tier - increase spend and commitment",
        "action":  "Loyalty tier upgrade prompt and targeted upsell",
        "channel": "Email, in-app messaging, personalised landing page",
        "message": "Acknowledge their loyalty. Show them how close they are "
                   "to the top tier. Give them a reason to get there.",
        "offer":   "Double points event, almost VIP milestone reward, "
                   "category-specific discount on highest-spend area",
        "timing":  "Trigger when RFM score reaches threshold - not on a "
                   "calendar",
        "kpi":     "Upgrade rate to VIP, average order value, repeat "
                   "purchase rate",
        "risk":    "Generic messaging will feel hollow to customers who "
                   "already consider themselves loyal.",
    },
    "Loyal Regulars": {
        "priority": "HIGH", "priority_color": "#2E7D6A",
        "goal":    "Increase order frequency and average basket size",
        "action":  "Cross-sell campaigns based on purchase history",
        "channel": "Email, retargeting ads, in-app recommendations",
        "message": "Helpful and personalised. Based on what you usually buy "
                   "you might like this - not salesy, genuinely useful.",
        "offer":   "Bundle deals, complementary product recommendations, "
                   "category expansion incentive",
        "timing":  "Post-purchase follow-up 3 to 5 days after each order",
        "kpi":     "Cross-category purchase rate, basket size, order "
                   "frequency",
        "risk":    "Recommendations must be relevant. Poor personalisation "
                   "damages trust more than it helps.",
    },
    "Casual Shoppers": {
        "priority": "MEDIUM", "priority_color": "#4A6FA5",
        "goal":    "Increase visit frequency and build habit",
        "action":  "Re-engagement campaign with seasonal relevance",
        "channel": "Email, social retargeting, push notification",
        "message": "Light-touch and timely. Align messaging to seasons, "
                   "events, or restocks relevant to past purchases.",
        "offer":   "Limited-time offer, new arrival alert in favourite "
                   "category, it has been a while discount",
        "timing":  "Trigger at 45-day inactivity mark",
        "kpi":     "Reactivation rate, time between purchases, email open "
                   "rate",
        "risk":    "Too many re-engagement emails will push them to "
                   "unsubscribe.",
    },
    "Occasional Buyers": {
        "priority": "MEDIUM", "priority_color": "#4A6FA5",
        "goal":    "Re-engage before they lapse completely",
        "action":  "Targeted win-back offer with urgency",
        "channel": "Email, SMS if opted in, retargeting",
        "message": "Simple and direct. Acknowledge the gap without being "
                   "awkward. We have missed you - here is something to "
                   "come back for.",
        "offer":   "Time-limited 10 to 15 percent discount, free delivery "
                   "on next order, what is new since you left showcase",
        "timing":  "Trigger at 90-day inactivity mark. One series maximum.",
        "kpi":     "Win-back rate, cost per reactivation, subsequent order "
                   "rate",
        "risk":    "A discount without a reason feels cheap. Give them a "
                   "hook - a new product, a seasonal moment, a milestone.",
    },
    "Lapsed": {
        "priority": "LOW / EVALUATE", "priority_color": "#C0392B",
        "goal":    "Selective win-back - not all lapsed customers are worth "
                   "recovering",
        "action":  "Segment lapsed customers by historical value before "
                   "acting",
        "channel": "Email only - do not invest in paid channels for "
                   "low-value lapsed",
        "message": "Honest and human. A simple we would love to have you "
                   "back with a genuine reason to return outperforms "
                   "aggressive discounting.",
        "offer":   "For high-value lapsed: meaningful discount or exclusive "
                   "offer. For low-value lapsed: suppress from paid campaigns.",
        "timing":  "One win-back email at 6 months. If no response, move "
                   "to suppression list.",
        "kpi":     "Win-back rate by historical value band, ROI on "
                   "reactivation spend",
        "risk":    "Spending to reactivate customers who were never valuable "
                   "is a guaranteed loss. Prioritise by lifetime value first.",
    },
}

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

seg_df   = df[df["cluster_label"] == segment]
n        = len(seg_df)
pct      = n / len(df) * 100
recency  = seg_df["recency"].mean()
freq     = seg_df["frequency"].mean()
monetary = seg_df["monetary"].mean()
mon_disp = (f"\u00a3{row['monetary']:,.2f}" if curr != "items"
            else f"{monetary:,.0f} items")

st.markdown(f"""
<div class="card" style="display:flex; align-items:center;
                          gap:1rem; flex-wrap:wrap;">
    <div style="flex:1;">
        <div style="font-family:'DM Serif Display',serif; font-size:1.1rem;
                    color:#1B3A5C;">{segment}</div>
        <div style="font-size:0.8rem; color:#6B7A99; margin-top:0.2rem;">
            {n:,.0f} customers &nbsp;&middot;&nbsp; {pct:.1f}% of base
            &nbsp;&middot;&nbsp; Avg recency {recency:.0f} days
            &nbsp;&middot;&nbsp; Avg {freq:.1f} orders
            &nbsp;&middot;&nbsp; Avg spend {mon_disp}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

strat = strategies.get(segment, {})
if strat:
    st.markdown(f"""
    <div style="display:inline-block; background:{strat['priority_color']};
                color:#fff; padding:0.25rem 0.9rem; border-radius:20px;
                font-size:0.72rem; font-weight:600; letter-spacing:0.1em;
                text-transform:uppercase; margin: 1rem 0 0.5rem 0;">
        Priority: {strat['priority']}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.9rem;">
                Strategic Goal</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:1.2rem;">{strat['goal']}</p>
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">
                Recommended Action</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:1.2rem;">{strat['action']}</p>
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">
                Best Channels</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:0;">{strat['channel']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">
                Message Tone and Approach</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:1.2rem;">{strat['message']}</p>
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">
                Suggested Offer</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:1.2rem;">{strat['offer']}</p>
            <div style="font-family:'DM Serif Display',serif; font-size:0.95rem;
                        color:#1B3A5C; margin-bottom:0.5rem;">Timing</div>
            <p style="font-size:0.87rem; color:#4A5568; line-height:1.65;
                      margin-bottom:0;">{strat['timing']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr;
                gap:1rem; margin-top:0.5rem;">
        <div class="card-mist">
            <div style="font-size:0.72rem; text-transform:uppercase;
                        letter-spacing:0.07em; color:#6B7A99;
                        margin-bottom:0.4rem;">KPIs to Track</div>
            <div style="font-size:0.87rem; color:#2C3E50;
                        line-height:1.6;">{strat['kpi']}</div>
        </div>
        <div style="background:#FDF2F2; border-radius:10px;
                    padding:1.25rem 1.5rem;">
            <div style="font-size:0.72rem; text-transform:uppercase;
                        letter-spacing:0.07em; color:#922B21;
                        margin-bottom:0.4rem;">Watch Out For</div>
            <div style="font-size:0.87rem; color:#2C3E50;
                        line-height:1.6;">{strat['risk']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="insight" style="margin-top:1.5rem;">
    Head to <strong>Churn Risk Report</strong> to identify high-value
    customers who are starting to disengage - before it is too late
    to act.
</div>
""", unsafe_allow_html=True)

prev_next_nav("Marketing Targeting")