import streamlit as st

from utils.session import initialize_session, is_logged_in
from components.styles import apply_global_styles
from components.sidebar import show_sidebar

from pages.login import show_login_page
from pages.employee_dashboard import show_employee_dashboard
from pages.employee_profile import show_employee_profile
from pages.employee_attendance import show_employee_attendance
from pages.employee_leave import show_employee_leave
from pages.employee_performance import show_employee_performance
from pages.hr_performance import show_hr_performance
from pages.admin_dashboard import show_admin_dashboard
from pages.admin_hr import show_admin_hr
from pages.change_password import show_change_password
from pages.admin_departments import show_admin_departments


st.set_page_config(
    page_title="Smart Employee Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

initialize_session()


if not is_logged_in():

    # Login state
    apply_global_styles()

    # Hide the sidebar expand/collapse arrow on the login screen —
    # there's nothing in the sidebar yet since the user isn't
    # authenticated, so the toggle shouldn't be visible here.
    st.markdown(
        """
        <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    show_login_page()

    st.stop()


# Authenticated state
apply_global_styles()


role = st.session_state.get("role")

page = show_sidebar(role)


if role == "Employee":

    if page == "Dashboard":
        show_employee_dashboard()

    elif page == "My Profile":
        show_employee_profile()

    elif page == "Attendance":
        show_employee_attendance()

    elif page == "Leave":
        show_employee_leave()

    elif page == "Performance":
        show_employee_performance()

    else:
        st.title(page)
        st.info(f"{page} page is coming next.")

elif role == "HR":

    if page == "Dashboard":
        from pages.hr_dashboard import show_hr_dashboard
        show_hr_dashboard()

    elif page == "Employees":
        from pages.hr_employees import show_hr_employees
        show_hr_employees()

    elif page == "Attendance":
        from pages.hr_attendance import show_hr_attendance
        show_hr_attendance()

    elif page == "Leave":
        from pages.hr_leave import show_hr_leave
        show_hr_leave()

    elif page == "Performance":
        show_hr_performance()

    elif page == "Reports":
        from pages.hr_reports import show_hr_reports
        show_hr_reports()
    elif page == "Change Password":
        show_change_password()

    else:
        st.title(page)
        st.info(f"{page} page is coming next.")

if role == "Admin":

    if page == "Dashboard":
        show_admin_dashboard()

    elif page == "HR Management":
        show_admin_hr()
    
    elif page == "Department Management":
        show_admin_departments()
        
    elif page == "Change Password":
        show_change_password()

    else:
        st.title(page)