import streamlit as st


def metric_card(title, value, subtitle="", icon="📊"):

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.caption(title)
            st.markdown(f"### {value}")

        with col2:
            st.markdown(f"### {icon}")

        if subtitle:
            st.caption(subtitle)


def section_header(title, subtitle=None):

    st.subheader(title)

    if subtitle:
        st.caption(subtitle)