import streamlit as st

from utils.session import logout


def show_sidebar(role):

    with st.sidebar:

        st.title("👥 Smart Employee")
        st.caption("Intelligence System")

        st.divider()

        st.caption("CURRENT USER")

        st.write(
            f"👤 **{st.session_state.get('username', 'User')}**"
        )

        st.caption(role)

        st.divider()

        st.caption("NAVIGATION")

        # If a Quick Action button elsewhere set a target page,
        # apply it to the relevant radio's state before that radio
        # is instantiated below, then consume it so it only fires once.
        nav_target = st.session_state.pop("nav_target", None)

        if role == "Employee":

            options = [
                "Dashboard",
                "My Profile",
                "Attendance",
                "Leave",
                "Performance",
            ]

            if nav_target in options:
                st.session_state["employee_nav_radio"] = nav_target

            page = st.radio(
                "Employee Menu",
                options,
                key="employee_nav_radio",
                label_visibility="collapsed",
            )

        elif role == "HR":

            options = [
                "Dashboard",
                "Employees",
                "Attendance",
                "Leave","Performance",
                "Reports","AI Prediction","Change Password"
            ]

            if nav_target in options:
                st.session_state["hr_nav_radio"] = nav_target

            page = st.radio(
                "HR Menu",
                options,
                key="hr_nav_radio",
                label_visibility="collapsed",
            )

        elif role == "Admin":

            options = [
                "Dashboard",
                "HR Management","Department Management","Change Password"
            ]

            if nav_target in options:
                st.session_state["admin_nav_radio"] = nav_target

            page = st.radio(
                "Admin Menu",
                options,
                key="admin_nav_radio",
                label_visibility="collapsed",
            )

        else:

            page = None

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            logout()

        return page