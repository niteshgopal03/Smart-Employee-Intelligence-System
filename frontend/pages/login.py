import streamlit as st

from api.auth_api import login_user
from utils.session import set_user_session


def show_login_page():

    
    header_left, header_center, header_right = st.columns([0.5, 4, 0.5])

    with header_center:
        st.markdown(
            "<div style='text-align: center;'>"
            "<h1>👥 Smart Employee Intelligence System</h1>"
            "<p style='color: #6b7280; font-size: 16px;'>"
            "Employee Management & Intelligence Platform"
            "</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    # Login Card
    left, center, right = st.columns([1, 1.4, 1])

    with center:
        with st.container(border=True):

            st.subheader("Welcome back")
            st.caption("Sign in to continue to your portal.")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            st.write("")

            login_clicked = st.button(
                "🔐 Sign in",
                type="primary",
                use_container_width=True,
            )

            if login_clicked:

                if not username.strip() or not password:
                    st.warning("Please enter username and password.")
                    return

                with st.spinner("Signing you in..."):

                    result = login_user(
                        username.strip(),
                        password,
                    )

                if result["success"]:

                    data = result["data"]

                    set_user_session(
                        data,
                        username.strip(),
                    )

                    st.rerun()

                else:
                    st.error(result["message"])