import os
import streamlit as st


try:
    API_BASE_URL = st.secrets["API_BASE_URL"]
except Exception:
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:8000"
    )