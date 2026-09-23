import streamlit as st

from api.client import api_request
from components.cards import section_header


def show_employee_profile():

    st.title("My Profile")
    st.caption("View your personal and employment information.")

    data, error = api_request("GET", "/employee/me")

    if error:
        st.error(error)
        return

    if not data:
        st.warning("No profile information found.")
        return

    employee = data.get("employee", data)

    first_name = employee.get("first_name", "")
    last_name = employee.get("last_name", "")

    full_name = f"{first_name} {last_name}".strip()

    if not full_name:
        full_name = "—"

    # ---------------------------------------------------------
    # Personal Information
    # ---------------------------------------------------------

    section_header(
        "Personal Information",
        "Your registered personal and contact details.",
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 👤 Basic Details")

            st.write(
                f"**Employee ID**  \n"
                f"{employee.get('employee_id', '—')}"
            )

            st.write(
                f"**Full Name**  \n"
                f"{full_name}"
            )

            st.write(
                f"**Gender**  \n"
                f"{employee.get('gender', '—')}"
            )

            st.write(
                f"**Date of Birth**  \n"
                f"{employee.get('dob', '—')}"
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### 📧 Contact Information")

            st.write(
                f"**Email**  \n"
                f"{employee.get('email', '—')}"
            )

            st.write(
                f"**Phone**  \n"
                f"{employee.get('phone', '—')}"
            )

    st.write("")

    # ---------------------------------------------------------
    # Employment Information
    # ---------------------------------------------------------

    section_header(
        "Employment Information",
        "Your current organization and employment details.",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("Department")

            department = employee.get("department")

            st.markdown(
                f"### {department if department else '—'}"
            )

    with col2:
        with st.container(border=True):
            st.caption("Designation")

            designation = employee.get("designation")

            st.markdown(
                f"### {designation if designation else '—'}"
            )

    with col3:
        with st.container(border=True):
            st.caption("Status")

            status = employee.get("status", "—")

            if str(status).lower() == "active":
                st.success(status)
            elif str(status).lower() in ["inactive", "resigned"]:
                st.warning(status)
            else:
                st.info(status)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 📅 Joining Information")

            st.write(
                f"**Joining Date**  \n"
                f"{employee.get('joining_date', '—')}"
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### 🎓 Education")

            st.write(
                employee.get("education", "—")
            )

    st.write("")

    # ---------------------------------------------------------
    # Skills
    # ---------------------------------------------------------

    section_header(
        "Skills",
        "Skills registered in your employee profile.",
    )

    with st.container(border=True):
        skills = employee.get("skills")

        if skills:
            st.write(skills)
        else:
            st.caption("No skills have been added to your profile.")

    st.write("")

    # ---------------------------------------------------------
    # Change Password
    # ---------------------------------------------------------

    section_header(
        "Account Security",
        "Update your account password.",
    )

    with st.container(border=True):

        st.markdown("#### 🔐 Change Password")

        current_password = st.text_input(
            "Current Password",
            type="password",
            placeholder="Enter your current password",
            key="current_password",
        )

        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Enter your new password",
            key="new_password",
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Re-enter your new password",
            key="confirm_password",
        )

        st.write("")

        if st.button(
            "🔒 Change Password",
            type="primary",
            use_container_width=True,
        ):

            if not current_password or not new_password or not confirm_password:
                st.warning("Please fill in all password fields.")
                return

            if new_password != confirm_password:
                st.error("New password and confirmation password do not match.")
                return

            if current_password == new_password:
                st.warning(
                    "New password must be different from your current password."
                )
                return

            password_data = {
                "current_password": current_password,
                "new_password": new_password,
            }

            with st.spinner("Updating password..."):

                result, error = api_request(
                    "PUT",
                    "/employee/me/password",
                    json=password_data,
                )

            if error:
                st.error(error)
                return

            message = (
                result.get("message", "Password changed successfully.")
                if isinstance(result, dict)
                else "Password changed successfully."
            )

            st.success(message)

            st.session_state.current_password = ""
            st.session_state.new_password = ""
            st.session_state.confirm_password = ""