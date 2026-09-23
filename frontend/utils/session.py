import streamlit as st


def initialize_session():

    defaults = {
        "access_token": None,
        "role": None,
        "employee_id": None,
        "username": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def is_logged_in():

    return (
        st.session_state.get("access_token")
        is not None
    )


def set_user_session(data, username):

    st.session_state.access_token = data.get(
        "access_token"
    )

    st.session_state.role = data.get(
        "role"
    )

    st.session_state.employee_id = data.get(
        "employee_id"
    )

    st.session_state.username = username


def logout():

    st.session_state.access_token = None
    st.session_state.role = None
    st.session_state.employee_id = None
    st.session_state.username = None

    st.rerun()