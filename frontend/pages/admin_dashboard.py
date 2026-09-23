
import streamlit as st

from api.client import api_request
from components.cards import metric_card


def show_admin_dashboard():

    st.title("🛡️ Admin Control Center") 
    st.caption("Monitor employees, departments, attendance, leave, and accounts.")

   

    data, error = api_request(
        "GET",
        "/dashboard/admin"
    )

    if error:
        st.error(error)
        return

    if not data:
        st.warning("No dashboard data available.")
        return

    employee = data.get("employee_overview") or {}
    departments = data.get("department_summary") or []
    attendance = data.get("today_attendance") or {}
    leave = data.get("leave_overview") or {}
    users = data.get("user_overview") or {}
    salary = data.get("salary_overview") or {}

    # =========================================================
    # PLATFORM SNAPSHOT
    # =========================================================

    st.markdown("### Platform Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Total Employees",
            employee.get("total_employees", 0) or 0,
            "All employee records",
            "👥",
        )

    with col2:
        metric_card(
            "Active Employees",
            employee.get("active_employees", 0) or 0,
            "Currently active",
            "🟢",
        )

    with col3:
        metric_card(
            "Departments",
            len(departments),
            "Organizational units",
            "🏢",
        )

    with col4:
        metric_card(
            "System Users",
            users.get("total_users", 0) or 0,
            "Registered accounts",
            "🔐",
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # =========================================================
    # EMPLOYEE STATUS
    # =========================================================

    with st.container(border=True):

        st.markdown("### 👥 Workforce Overview")
        st.caption("Current employee distribution across the organization.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Employees",
                employee.get("total_employees", 0) or 0,
            )

        with col2:
            st.metric(
                "Active Employees",
                employee.get("active_employees", 0) or 0,
            )

        with col3:
            st.metric(
                "Resigned Employees",
                employee.get("resigned_employees", 0) or 0,
            )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # =========================================================
    # ATTENDANCE + LEAVE
    # =========================================================

    left, right = st.columns(2)

    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------

    with left:

        with st.container(border=True):

            st.markdown("### 🕒 Today's Attendance")
            st.caption("Attendance records for the current day.")

            total = attendance.get("total", 0) or 0
            present = attendance.get("present", 0) or 0
            absent = attendance.get("absent", 0) or 0
            leave_count = attendance.get("leave_count", 0) or 0

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Present", present)

            with c2:
                st.metric("Absent", absent)

            with c3:
                st.metric("Leave", leave_count)

            if total > 0:

                attendance_percentage = (
                    present / total
                ) * 100

                st.markdown("")

                st.progress(
                    min(attendance_percentage / 100, 1.0)
                )

                st.caption(
                    f"Present attendance rate: "
                    f"**{attendance_percentage:.1f}%**"
                )

            else:
                st.info(
                    "No attendance records available for today."
                )

    # ---------------------------------------------------------
    # LEAVE
    # ---------------------------------------------------------

    with right:

        with st.container(border=True):

            st.markdown("### 📋 Leave Overview")
            st.caption("Current leave request distribution.")

            total_requests = (
                leave.get("total_requests", 0) or 0
            )

            pending = leave.get("pending", 0) or 0
            approved = leave.get("approved", 0) or 0
            rejected = leave.get("rejected", 0) or 0

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Total Requests",
                    total_requests
                )

            with c2:
                st.metric(
                    "Pending",
                    pending
                )

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Approved",
                    approved
                )

            with c2:
                st.metric(
                    "Rejected",
                    rejected
                )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # =========================================================
    # USERS + SALARY
    # =========================================================

    left, right = st.columns(2)

    # ---------------------------------------------------------
    # USER ACCOUNTS
    # ---------------------------------------------------------

    with left:

        with st.container(border=True):

            st.markdown("### 🔐 User Accounts")
            st.caption("Distribution of system accounts by role.")

            total_users = users.get("total_users", 0) or 0
            admin_users = users.get("admin_users", 0) or 0
            hr_users = users.get("hr_users", 0) or 0
            employee_users = users.get("employee_users", 0) or 0
            active_users = users.get("active_users", 0) or 0

            st.metric(
                "Active Accounts",
                active_users
            )

            st.markdown("")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Admins",
                    admin_users
                )

            with c2:
                st.metric(
                    "HR",
                    hr_users
                )

            with c3:
                st.metric(
                    "Employees",
                    employee_users
                )

            st.caption(
                f"Total system accounts: {total_users}"
            )

    # ---------------------------------------------------------
    # SALARY
    # ---------------------------------------------------------

    with right:

        with st.container(border=True):

            st.markdown("### 💰 Salary Overview")
            st.caption("Salary information for active employees.")

            total_salary = (
                salary.get("total_salary", 0) or 0
            )

            average_salary = (
                salary.get("average_salary", 0) or 0
            )

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Average Salary",
                    f"₹{average_salary:,.0f}"
                )

            with c2:
                st.metric(
                    "Total Salary",
                    f"₹{total_salary:,.0f}"
                )

            st.markdown("")

            if total_salary > 0:

                st.progress(1.0)

                st.caption(
                    "Salary overview is based on the active "
                    "employee records returned by the dashboard API."
                )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # =========================================================
    # DEPARTMENT ANALYTICS
    # =========================================================

    st.markdown("### 🏢 Department Analytics")
    st.caption("Employee distribution across organizational departments.")

    if departments:

        chart_data = []

        for department in departments:

            chart_data.append(
                {
                    "Department": department.get(
                        "department_name",
                        "Unknown"
                    ),
                    "Employees": int(
                        department.get(
                            "employee_count",
                            0
                        ) or 0
                    ),
                }
            )

        st.bar_chart(
            chart_data,
            x="Department",
            y="Employees",
            use_container_width=True,
        )

        st.markdown("")

        with st.container(border=True):

            st.markdown("#### Department Details")

            st.dataframe(
                departments,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "department_name": st.column_config.TextColumn(
                        "Department"
                    ),
                    "employee_count": st.column_config.NumberColumn(
                        "Employees"
                    ),
                },
            )

    else:

        st.info(
            "No department information available."
        )

    # =========================================================
    # REFRESH
    # =========================================================

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True,
        ):
            st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#9ca3af;
            font-size:12px;
            margin-top:14px;
        ">
            Smart Employee Intelligence System · Admin Workspace
        </div>
        """,
        unsafe_allow_html=True,
    )