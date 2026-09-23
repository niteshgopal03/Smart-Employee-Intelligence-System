import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN THEME — deep ocean blue, calm & professional
           ===================================================== */

        .stApp {
            background: radial-gradient(circle at 20% 0%, #0f2540 0%, #0a1a2f 45%, #071220 100%) !important;
            color: #eaf2fb !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        .main {
            background: transparent !important;
        }

        .main .block-container {
            background: transparent !important;
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Streamlit's own top toolbar (hamburger menu / status icon) —
           make it blend into the app background instead of showing
           as a solid black bar, and keep its icons visible on dark. */
        [data-testid="stHeader"] {
            background: transparent !important;
            background-color: rgba(0, 0, 0, 0) !important;
        }

        [data-testid="stHeader"] * {
            color: #eaf2fb !important;
            fill: #eaf2fb !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }


        /* =====================================================
           TEXT
           ===================================================== */

        h1,
        h2,
        h3,
        h4,
        h5,
        p,
        label {
            color: #eaf2fb !important;
        }

        /* Solid heading color instead of a background-clip gradient —
           the gradient-text trick strips native color out of emoji
           (breaking logos) and interferes with Streamlit's built-in
           heading anchor-link icon, so we avoid it entirely. */
        h1, h2, h3 {
            color: #38bdf8 !important;
        }

        /* Permanently hide Streamlit's heading anchor-link icon.
           Different Streamlit versions render this with different
           markup, so several selectors are covered here rather than
           relying on hover-to-reveal, which wasn't taking effect. */
        [data-testid="stHeaderActionElements"],
        [data-testid="stElementToolbar"],
        .stMarkdown h1 a,
        .stMarkdown h2 a,
        .stMarkdown h3 a,
        .stMarkdown h4 a,
        h1 > a,
        h2 > a,
        h3 > a,
        h4 > a {
            display: none !important;
        }

        [data-testid="stCaptionContainer"] {
            color: #90a9c4 !important;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0c1f38 0%,
                    #103a5c 55%,
                    #0e5266 100%
                ) !important;

            border-right: 1px solid rgba(56,189,248,0.18);
        }

        section[data-testid="stSidebar"] * {
            color: #dceafb !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(56,189,248,0.25) !important;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"] {
            gap: 6px;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"] label {
            background: rgba(56,189,248,0.08);
            border: 1px solid transparent;
            border-radius: 11px;
            padding: 9px 12px;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"] label:hover {
            background: rgba(45,212,191,0.14);
            border-color: rgba(45,212,191,0.35);
        }


        /* =====================================================
           CARDS / BORDERED CONTAINERS
           ===================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(160deg, #122c47 0%, #0d2136 100%) !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            border-radius: 18px !important;
            box-shadow: 0 8px 28px rgba(8,47,73,0.45) !important;
        }


        /* =====================================================
           METRICS
           ===================================================== */

        div[data-testid="stMetric"] {
            background: linear-gradient(160deg, #122c47 0%, #0d2136 100%) !important;
            border: 1px solid rgba(45,212,191,0.25) !important;
            border-radius: 16px !important;
            padding: 18px 20px !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #90a9c4 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #38bdf8 !important;
            font-weight: 800 !important;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stTextArea textarea {
            background: #0d2136 !important;
            color: #eaf2fb !important;
            border: 1px solid #234a6b !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }

        .stTextInput input::placeholder,
        .stNumberInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #5d7c9a !important;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stTimeInput input:focus,
        .stTextArea textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow:
                0 0 0 3px rgba(56,189,248,0.20) !important;
        }


        /* =====================================================
           SELECTBOX / MULTISELECT
           ===================================================== */

        div[data-baseweb="select"] > div {
            background: #0d2136 !important;
            border-color: #234a6b !important;
            border-radius: 10px !important;
        }

        div[data-baseweb="select"] span {
            color: #eaf2fb !important;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            background: linear-gradient(90deg, #0ea5e9 0%, #2dd4bf 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            min-height: 42px;
            font-weight: 700 !important;
            box-shadow:
                0 6px 18px rgba(14,165,233,0.30);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #38bdf8 0%, #5eead4 100%) !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow:
                0 10px 26px rgba(45,212,191,0.35);
        }


        /* =====================================================
           EXPANDERS
           ===================================================== */

        details {
            background: linear-gradient(160deg, #122c47 0%, #0d2136 100%) !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            border-radius: 14px !important;
        }

        details summary {
            color: #eaf2fb !important;
            font-weight: 700 !important;
        }


        /* =====================================================
           TABS
           ===================================================== */

        button[data-baseweb="tab"] {
            color: #90a9c4 !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #2dd4bf !important;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 12px !important;
        }


        /* =====================================================
           DATAFRAME
           ===================================================== */

        div[data-testid="stDataFrame"] {
            background: linear-gradient(160deg, #122c47 0%, #0d2136 100%) !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            border-radius: 14px !important;
            overflow: hidden;
        }


        /* =====================================================
           CHECKBOX / RADIO
           ===================================================== */

        div[data-testid="stCheckbox"] label,
        .stRadio label {
            color: #cbd5e1 !important;
        }


        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {
            border-color: rgba(56,189,248,0.25) !important;
        }


        /* =====================================================
           SCROLLBAR
           ===================================================== */

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #0a1a2f;
        }

        ::-webkit-scrollbar-thumb {
            background: #234a6b;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #38bdf8;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )