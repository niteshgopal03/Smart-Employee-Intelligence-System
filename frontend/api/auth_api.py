import requests

from config import API_BASE_URL


def login_user(username, password):

    try:

        response = requests.post(
            f"{API_BASE_URL}/login",
            json={
                "username": username,
                "password": password
            },
            timeout=10
        )

    except requests.exceptions.RequestException:

        return {
            "success": False,
            "message": "Unable to connect to backend."
        }

    try:

        data = response.json()

    except Exception:

        return {
            "success": False,
            "message": "Invalid response from backend."
        }

    if response.status_code != 200:

        return {
            "success": False,
            "message": data.get(
                "message",
                data.get(
                    "detail",
                    "Login failed."
                )
            )
        }

    if "access_token" not in data:

        return {
            "success": False,
            "message": data.get(
                "message",
                "Login failed."
            )
        }

    return {
        "success": True,
        "data": data
    }