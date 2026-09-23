import requests
import streamlit as st

from config import API_BASE_URL


def api_request(method, endpoint, **kwargs):

    headers = kwargs.pop("headers", {})

    token = st.session_state.get("access_token")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:

        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            headers=headers,
            timeout=10,
            **kwargs
        )

    except requests.exceptions.RequestException as e:

        return None, f"Unable to connect to backend: {e}"

    # Do NOT logout automatically here.
    # We need to see which endpoint/authentication check is failing.
    if response.status_code == 401:

        try:
            data = response.json()
            message = data.get(
                "detail",
                data.get("message", "Unauthorized request.")
            )
        except Exception:
            message = "Unauthorized request."

        return None, f"Authentication error: {message}"

    if response.status_code >= 400:

        try:
            data = response.json()

            message = data.get(
                "detail",
                data.get("message", "Request failed.")
            )

        except Exception:

            message = "Request failed."

        return None, message

    try:

        return response.json(), None

    except Exception:

        return response.text, None
