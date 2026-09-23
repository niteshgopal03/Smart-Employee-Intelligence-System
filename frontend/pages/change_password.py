import streamlit as st

from api.client import api_request


def show_change_password():

    st.title("🔐 Change Password")
    st.caption("Update your account password securely.")

    role = st.session_state.get("role", "User")
    username = st.session_state.get("username", "User")

    left, center, right = st.columns([1, 1.6, 1])

    with center:

        with st.container(border=True):

            st.markdown("### 🔐 Account Security")

            st.caption(
                f"Logged in as **{username}** · {role}"
            )

            st.markdown("")

            current_password = st.text_input(
                "Current Password",
                type="password",
                placeholder="Enter your current password",
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter your new password",
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Re-enter your new password",
            )

            st.markdown("")

            st.caption(
                "Password must contain at least 6 characters."
            )

            if st.button(
                "🔒 Update Password",
                use_container_width=True,
                type="primary",
            ):

                if not current_password:
                    st.error("Please enter your current password.")
                    return

                if not new_password:
                    st.error("Please enter a new password.")
                    return

                if len(new_password) < 6:
                    st.error(
                        "New password must contain at least 6 characters."
                    )
                    return

                if new_password != confirm_password:
                    st.error(
                        "New password and confirmation do not match."
                    )
                    return

                if new_password == current_password:
                    st.error(
                        "New password must be different from the current password."
                    )
                    return

                payload = {
                    "current_password": current_password,
                    "new_password": new_password,
                }

                data, error = api_request(
                    "PUT",
                    "/auth/change-password",
                    json=payload,
                )

                if error:
                    st.error(error)
                    return

                message = (
                    data.get(
                        "message",
                        "Password changed successfully."
                    )
                    if isinstance(data, dict)
                    else "Password changed successfully."
                )

                st.success(message)

                st.info(
                    "Your new password will be used the next time you log in."
                )