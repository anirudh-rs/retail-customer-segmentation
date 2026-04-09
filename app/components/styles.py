import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --navy:   #1B3A5C;
        --slate:  #4A6FA5;
        --mist:   #EEF2F7;
        --cloud:  #F7F9FC;
        --ink:    #1A1F2E;
        --mid:    #6B7A99;
        --accent: #C8873A;
        --green:  #2E7D6A;
        --red:    #C0392B;
        --border: #DDE3EE;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
        background-color: var(--cloud);
    }

    section[data-testid="stSidebar"] {
        background: var(--navy) !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] * {
        color: #CBD8EC !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        color: var(--navy) !important;
        font-weight: 400 !important;
    }

    .card {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
    }
    .card-mist {
        background: var(--mist);
        border: none;
        border-radius: 10px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .kpi-tile {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        text-align: center;
    }
    .kpi-tile .kpi-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: var(--navy);
        line-height: 1.1;
    }
    .kpi-tile .kpi-label {
        font-size: 0.75rem;
        color: var(--mid);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.35rem;
    }
    .kpi-tile .kpi-sub {
        font-size: 0.8rem;
        color: var(--slate);
        margin-top: 0.2rem;
    }

    .chapter {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.4rem;
    }

    .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 2rem 0;
    }

    .badge {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.03em;
    }
    .badge-vip    { background: #FEF3E2; color: #B45309; }
    .badge-champ  { background: #EDF7F4; color: #1A6B57; }
    .badge-loyal  { background: #EBF2FB; color: #1B4F8A; }
    .badge-lapsed { background: #FDF2F2; color: #922B21; }

    .metric-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .metric-box {
        flex: 1;
        min-width: 120px;
        background: var(--mist);
        border-radius: 8px;
        padding: 0.85rem 1rem;
        text-align: center;
    }
    .metric-box .m-val {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: var(--navy);
    }
    .metric-box .m-lbl {
        font-size: 0.7rem;
        color: var(--mid);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-top: 0.2rem;
    }

    .insight {
        border-left: 3px solid var(--accent);
        padding: 0.75rem 1rem;
        background: #FFFBF5;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: var(--ink);
        margin: 1rem 0;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {background: transparent;}

    .stSelectbox label, .stRadio label {
        font-size: 0.82rem !important;
        color: var(--mid) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }
    .styled-table th {
        background: var(--navy);
        color: #fff;
        padding: 0.6rem 0.9rem;
        text-align: left;
        font-weight: 500;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .styled-table td {
        padding: 0.55rem 0.9rem;
        border-bottom: 1px solid var(--border);
        color: var(--ink);
    }
    .styled-table tr:last-child td { border-bottom: none; }
    .styled-table tr:hover td { background: var(--mist); }

    div[data-testid="stPageLink"] a {
        background: transparent;
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.4rem 1rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--mid) !important;
        text-decoration: none;
        transition: all 0.15s ease;
    }
    div[data-testid="stPageLink"] a:hover {
        background: var(--mist);
        color: var(--navy) !important;
        border-color: var(--navy);
    }
    div[data-testid="stPageLink-active"] a {
        background: var(--navy) !important;
        color: #fff !important;
        border-color: var(--navy) !important;
    }
    </style>
    """, unsafe_allow_html=True)


PAGE_DESCRIPTIONS = {
    "Home": (
        "Introduction",
        "The business case for customer segmentation and an overview "
        "of what this project covers."
    ),
    "Data Overview": (
        "The Data",
        "Three real-world datasets, 62M+ transactions cleaned and "
        "standardised into a single schema."
    ),
    "Segment Explorer": (
        "The Segments",
        "RFM scoring and K-Means clustering reveal four distinct "
        "customer behaviour tiers per retailer."
    ),
    "Marketing Targeting": (
        "The Strategy",
        "Tailored marketing actions, channels, and offers for each "
        "customer segment."
    ),
    "Churn Risk Report": (
        "The Warning List",
        "High-value customers going cold are flagged automatically "
        "and exported for immediate action."
    ),
    "Customer Lookup": (
        "The Individual",
        "Look up any customer to see their full RFM profile and "
        "personalised recommendation."
    ),
}

DATASET_STATS = [
    ("UCI Retail",  "5,878",       "customers"),
    ("H&M Fashion", "1,362,281",   "customers"),
    ("Instacart",   "206,209",     "customers"),
]


def sidebar_header(current_page="Home"):
    desc = PAGE_DESCRIPTIONS.get(current_page, ("", ""))
    with st.sidebar:
        st.markdown("""
        <div style='padding: 1.5rem 0 0.75rem 0;'>
            <div style='font-size:1.6rem; color:#fff;
                        font-family:"DM Serif Display",serif;
                        letter-spacing:0.02em; line-height:1.2;'>
                Retail<br>Intelligence
            </div>
            <div style='font-size:0.7rem; color:#7A9CC4; margin-top:0.4rem;
                        letter-spacing:0.1em; text-transform:uppercase;'>
                Customer Segmentation
            </div>
        </div>
        <hr/>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-bottom:1.25rem;'>
            <div style='font-size:0.68rem; color:#7A9CC4; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.4rem;'>
                Current Page
            </div>
            <div style='font-size:0.95rem; color:#fff;
                        font-family:"DM Serif Display",serif;
                        margin-bottom:0.35rem;'>
                {desc[0]}
            </div>
            <div style='font-size:0.78rem; color:#8AAACB; line-height:1.6;'>
                {desc[1]}
            </div>
        </div>
        <hr/>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-size:0.68rem; color:#7A9CC4; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.75rem;'>
            Dataset Stats
        </div>
        """, unsafe_allow_html=True)

        for name, value, label in DATASET_STATS:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between;
                        align-items:baseline; padding:0.35rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.06);'>
                <div style='font-size:0.78rem; color:#8AAACB;'>{name}</div>
                <div>
                    <span style='font-family:"DM Serif Display",serif;
                                 font-size:0.95rem; color:#fff;'>
                        {value}
                    </span>
                    <span style='font-size:0.68rem; color:#4A6A8A;
                                 margin-left:0.25rem;'>{label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:0.75rem; padding:0.35rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.06);
                    display:flex; justify-content:space-between;
                    align-items:baseline;'>
            <div style='font-size:0.78rem; color:#8AAACB;'>Transactions</div>
            <div>
                <span style='font-family:"DM Serif Display",serif;
                             font-size:0.95rem; color:#fff;'>62M+</span>
            </div>
        </div>
        <div style='padding:0.35rem 0; display:flex;
                    justify-content:space-between; align-items:baseline;'>
            <div style='font-size:0.78rem; color:#8AAACB;'>Clusters</div>
            <div>
                <span style='font-family:"DM Serif Display",serif;
                             font-size:0.95rem; color:#fff;'>4</span>
                <span style='font-size:0.68rem; color:#4A6A8A;
                             margin-left:0.25rem;'>per retailer</span>
            </div>
        </div>
        <hr/>
        <div style='font-size:0.68rem; color:#4A6A8A; line-height:1.7;
                    margin-top:0.25rem;'>
            K-Means clustering<br>
            RFM feature engineering<br>
            Silhouette + elbow method<br>
            Outlier capping at 99th pct
        </div>
        """, unsafe_allow_html=True)


def nav_bar(current_page):
    pages = [
        ("Home",      "Home"),
        ("Data",      "pages/1_Data_Overview"),
        ("Segments",  "pages/2_Segment_Explorer"),
        ("Targeting", "pages/3_Marketing_Targeting"),
        ("Churn",     "pages/4_Churn_Report"),
        ("Lookup",    "pages/5_Customer_Lookup"),
    ]
    cols = st.columns(len(pages))
    for col, (label, page) in zip(cols, pages):
        with col:
            st.page_link(
                f"{page}.py",
                label=label,
                use_container_width=True
            )


def prev_next_nav(current_page):
    pages = [
        ("Home",               "Home"),
        ("Data Overview",      "pages/1_Data_Overview"),
        ("Segment Explorer",   "pages/2_Segment_Explorer"),
        ("Marketing Targeting","pages/3_Marketing_Targeting"),
        ("Churn Risk Report",  "pages/4_Churn_Report"),
        ("Customer Lookup",    "pages/5_Customer_Lookup"),
    ]

    current_idx = next(
        (i for i, (label, _) in enumerate(pages) if label == current_page),
        0
    )

    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

    col_prev, col_mid, col_next = st.columns([1, 3, 1])

    with col_prev:
        if current_idx > 0:
            prev_label, prev_page = pages[current_idx - 1]
            prev_short = prev_label.split()[0]
            st.page_link(
                f"{prev_page}.py",
                label=f"Back: {prev_short}",
                use_container_width=True
            )

    with col_mid:
        st.markdown(
            f"<div style='text-align:center; font-size:0.78rem; "
            f"color:#6B7A99; padding-top:0.4rem;'>"
            f"Chapter {current_idx + 1} of {len(pages)}</div>",
            unsafe_allow_html=True
        )

    with col_next:
        if current_idx < len(pages) - 1:
            next_label, next_page = pages[current_idx + 1]
            next_short = next_label.split()[0]
            st.page_link(
                f"{next_page}.py",
                label=f"Next: {next_short}",
                use_container_width=True
            )