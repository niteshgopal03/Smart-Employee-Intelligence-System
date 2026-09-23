import streamlit as st

from api.client import api_request


def show_hr_dashboard():

    st.title("🧭 HR Command Center")
    st.caption(
        "A centralized view of workforce, attendance, leave, "
        "performance, departments, and salary insights."
    )

    st.write("")

    # ==================================================
    # LOAD HR REPORTS
    # ==================================================

    employees_data, employees_error = api_request(
        "GET",
        "/hr/reports/employees"
    )

    departments_data, departments_error = api_request(
        "GET",
        "/hr/reports/departments"
    )

    attendance_data, attendance_error = api_request(
        "GET",
        "/hr/reports/attendance"
    )

    leave_data, leave_error = api_request(
        "GET",
        "/hr/reports/leave"
    )

    performance_data, performance_error = api_request(
        "GET",
        "/hr/reports/performance"
    )

    salary_data, salary_error = api_request(
        "GET",
        "/hr/reports/salary"
    )

    # ==================================================
    # ERROR HANDLING
    # ==================================================

    api_errors = [
        ("Employees", employees_error),
        ("Departments", departments_error),
        ("Attendance", attendance_error),
        ("Leave", leave_error),
        ("Performance", performance_error),
        ("Salary", salary_error),
    ]

    failed_apis = [
        name
        for name, error in api_errors
        if error
    ]

    if failed_apis:
        st.error(
            "Unable to load: "
            + ", ".join(failed_apis)
        )
        return

    # ==================================================
    # NORMALIZE RESPONSES
    # ==================================================

    employees_data = (
        employees_data
        if isinstance(employees_data, dict)
        else {}
    )

    departments_data = (
        departments_data
        if isinstance(departments_data, dict)
        else {}
    )

    attendance_data = (
        attendance_data
        if isinstance(attendance_data, dict)
        else {}
    )

    leave_data = (
        leave_data
        if isinstance(leave_data, dict)
        else {}
    )

    performance_data = (
        performance_data
        if isinstance(performance_data, dict)
        else {}
    )

    salary_data = (
        salary_data
        if isinstance(salary_data, dict)
        else {}
    )

    # ==================================================
    # EMPLOYEE REPORT
    # Backend:
    # {
    #   total_employees,
    #   active_employees,
    #   resigned_employees
    # }
    # ==================================================

    total_employees = (
        employees_data.get("total_employees") or 0
    )

    active_employees = (
        employees_data.get("active_employees") or 0
    )

    resigned_employees = (
        employees_data.get("resigned_employees") or 0
    )

    # ==================================================
    # DEPARTMENT REPORT
    # Backend:
    # {
    #   departments: [...]
    # }
    # ==================================================

    departments = departments_data.get(
        "departments",
        []
    )

    if not isinstance(departments, list):
        departments = []

    total_departments = len(departments)

    # ==================================================
    # ATTENDANCE REPORT
    # Backend:
    # {
    #   total_records,
    #   present,
    #   absent,
    #   leave,
    #   attendance_percentage
    # }
    # ==================================================

    total_attendance = (
        attendance_data.get("total_records") or 0
    )

    present = (
        attendance_data.get("present") or 0
    )

    absent = (
        attendance_data.get("absent") or 0
    )

    leave_attendance = (
        attendance_data.get("leave") or 0
    )

    attendance_percentage = (
        attendance_data.get("attendance_percentage") or 0
    )

    # ==================================================
    # LEAVE REPORT
    # Backend:
    # {
    #   total_requests,
    #   pending,
    #   approved,
    #   rejected,
    #   approved_leave_days
    # }
    # ==================================================

    total_leave = (
        leave_data.get("total_requests") or 0
    )

    pending_leave = (
        leave_data.get("pending") or 0
    )

    approved_leave = (
        leave_data.get("approved") or 0
    )

    rejected_leave = (
        leave_data.get("rejected") or 0
    )

    approved_leave_days = (
        leave_data.get("approved_leave_days") or 0
    )

    # ==================================================
    # PERFORMANCE REPORT
    # Backend:
    # {
    #   summary: {
    #       rated_employees,
    #       average_rating,
    #       highest_rating,
    #       lowest_rating
    #   },
    #   department_statistics: [...]
    # }
    # ==================================================

    performance_summary = performance_data.get(
        "summary",
        {}
    )

    if not isinstance(performance_summary, dict):
        performance_summary = {}

    rated_employees = (
        performance_summary.get("rated_employees") or 0
    )

    average_rating = (
        performance_summary.get("average_rating") or 0
    )

    highest_rating = (
        performance_summary.get("highest_rating") or 0
    )

    lowest_rating = (
        performance_summary.get("lowest_rating") or 0
    )

    # ==================================================
    # SALARY REPORT
    # Backend:
    # {
    #   summary: {
    #       employees_with_salary,
    #       average_salary,
    #       minimum_salary,
    #       maximum_salary,
    #       total_salary
    #   },
    #   department_statistics: [...]
    # }
    # ==================================================

    salary_summary = salary_data.get(
        "summary",
        {}
    )

    if not isinstance(salary_summary, dict):
        salary_summary = {}

    salary_records = (
        salary_summary.get("employees_with_salary") or 0
    )

    total_salary = (
        salary_summary.get("total_salary") or 0
    )

    average_salary = (
        salary_summary.get("average_salary") or 0
    )

    minimum_salary = (
        salary_summary.get("minimum_salary") or 0
    )

    maximum_salary = (
        salary_summary.get("maximum_salary") or 0
    )

    # ==================================================
    # HERO SECTION
    # ==================================================

    with st.container(border=True):

        left, middle, right = st.columns(
            [2.2, 1, 1]
        )

        with left:

            st.markdown(
                "### 👋 HR Overview"
            )

            st.write(
                "Monitor the organization from one "
                "centralized workforce intelligence view."
            )

        with middle:

            st.caption("ACTIVE WORKFORCE")

            st.markdown(
                f"## {active_employees}"
            )

            st.caption(
                f"of {total_employees} employees"
            )

        with right:

            st.caption("DEPARTMENTS")

            st.markdown(
                f"## {total_departments}"
            )

            st.caption(
                "Organizational units"
            )

    st.write("")
    st.write("")

    # ==================================================
    # WORKFORCE SNAPSHOT
    # ==================================================

    st.subheader("Workforce Snapshot")

    st.caption(
        "High-level indicators from the HR reporting system."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        with st.container(border=True):

            st.caption("👥 EMPLOYEES")

            st.markdown(
                f"## {total_employees}"
            )

            st.caption(
                f"{active_employees} active"
            )

    with col2:

        with st.container(border=True):

            st.caption("📅 ATTENDANCE")

            st.markdown(
                f"## {float(attendance_percentage):.1f}%"
            )

            st.progress(
                min(
                    max(
                        float(attendance_percentage) / 100,
                        0
                    ),
                    1
                )
            )

            st.caption(
                f"{present} present / "
                f"{total_attendance} records"
            )

    with col3:

        with st.container(border=True):

            st.caption("🏖️ LEAVE")

            st.markdown(
                f"## {total_leave}"
            )

            st.caption(
                f"{pending_leave} pending requests"
            )

    with col4:

        with st.container(border=True):

            st.caption("📈 PERFORMANCE")

            st.markdown(
                f"## {float(average_rating):.2f}"
            )

            st.caption(
                f"{rated_employees} rated employees"
            )

    st.write("")
    st.write("")

    # ==================================================
    # ATTENDANCE + LEAVE
    # ==================================================

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.markdown(
                "### 📅 Attendance Pulse"
            )

            st.caption(
                "Current attendance report summary."
            )

            attendance_col1, attendance_col2 = st.columns(2)

            with attendance_col1:

                st.metric(
                    "Present",
                    present
                )

                st.metric(
                    "Absent",
                    absent
                )

            with attendance_col2:

                st.metric(
                    "Leave",
                    leave_attendance
                )

                st.metric(
                    "Total Records",
                    total_attendance
                )

    with right:

        with st.container(border=True):

            st.markdown(
                "### 🏖️ Leave Pulse"
            )

            st.caption(
                "Current leave request distribution."
            )

            leave_col1, leave_col2 = st.columns(2)

            with leave_col1:

                st.metric(
                    "Pending",
                    pending_leave
                )

                st.metric(
                    "Approved",
                    approved_leave
                )

            with leave_col2:

                st.metric(
                    "Rejected",
                    rejected_leave
                )

                st.metric(
                    "Total",
                    total_leave
                )

    st.write("")
    st.write("")

    # ==================================================
    # PERFORMANCE OVERVIEW
    # ==================================================

    st.subheader("📈 Performance Overview")

    st.caption(
        "Organization-wide performance statistics."
    )

    performance_col1, performance_col2, performance_col3 = st.columns(3)

    with performance_col1:

        with st.container(border=True):

            st.caption("RATED EMPLOYEES")

            st.markdown(
                f"## {rated_employees}"
            )

            st.caption(
                "Employees with performance ratings"
            )

    with performance_col2:

        with st.container(border=True):

            st.caption("AVERAGE RATING")

            st.markdown(
                f"## {float(average_rating):.2f}"
            )

            st.caption(
                "Organization average"
            )

    with performance_col3:

        with st.container(border=True):

            st.caption("RATING RANGE")

            st.markdown(
                f"## {float(lowest_rating):.1f} – "
                f"{float(highest_rating):.1f}"
            )

            st.caption(
                "Lowest to highest rating"
            )

    st.write("")
    st.write("")

    # ==================================================
    # SALARY OVERVIEW
    # ==================================================

    st.subheader("💰 Compensation Overview")

    st.caption(
        "Salary statistics returned by the HR reporting system."
    )

    salary_col1, salary_col2, salary_col3 = st.columns(3)

    with salary_col1:

        with st.container(border=True):

            st.caption("TOTAL SALARY")

            st.markdown(
                f"## ₹{float(total_salary):,.0f}"
            )

            st.caption(
                "Combined salary value"
            )

    with salary_col2:

        with st.container(border=True):

            st.caption("AVERAGE SALARY")

            st.markdown(
                f"## ₹{float(average_salary):,.0f}"
            )

            st.caption(
                "Average salary"
            )

    with salary_col3:

        with st.container(border=True):

            st.caption("SALARY RECORDS")

            st.markdown(
                f"## {salary_records}"
            )

            st.caption(
                f"Range: ₹{float(minimum_salary):,.0f}"
                f" – ₹{float(maximum_salary):,.0f}"
            )

    st.write("")
    st.write("")

    # ==================================================
    # ORGANIZATION OVERVIEW
    # ==================================================

    st.subheader("🏢 Organization Overview")

    st.caption(
        "Current workforce structure."
    )

    org_col1, org_col2, org_col3 = st.columns(3)

    with org_col1:

        with st.container(border=True):

            st.caption("TOTAL EMPLOYEES")

            st.markdown(
                f"## {total_employees}"
            )

            st.caption(
                "All employee records"
            )

    with org_col2:

        with st.container(border=True):

            st.caption("ACTIVE")

            st.markdown(
                f"## {active_employees}"
            )

            st.caption(
                "Active workforce"
            )

    with org_col3:

        with st.container(border=True):

            st.caption("RESIGNED")

            st.markdown(
                f"## {resigned_employees}"
            )

            st.caption(
                "Resigned employees"
            )

    st.write("")
    st.write("")

    # ==================================================
    # DEPARTMENT OVERVIEW
    # ==================================================

    st.subheader("🏢 Department Overview")

    st.caption(
        "Departments returned by the HR reporting system."
    )

    if departments:

        department_table = []

        for department in departments:

            department_table.append(
                {
                    "Department ID": department.get(
                        "department_id",
                        "—"
                    ),
                    "Department": department.get(
                        "department_name",
                        "—"
                    ),
                    "Employees": department.get(
                        "total_employees",
                        0
                    ),
                    "Active": department.get(
                        "active_employees",
                        0
                    ),
                    "Resigned": department.get(
                        "resigned_employees",
                        0
                    ),
                }
            )

        st.dataframe(
            department_table,
            use_container_width=True,
            hide_index=True,
        )

    else:

        with st.container(border=True):

            st.info(
                "No department records found."
            )

    st.write("")
    st.write("")

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.subheader("⚡ HR Actions")

    st.caption(
        "Move quickly to the most frequently used HR modules."
    )

    action1, action2, action3, action4 = st.columns(4)

    with action1:

        if st.button(
            "👥 Employees",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Employees"
            st.rerun()

    with action2:

        if st.button(
            "📅 Attendance",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Attendance"
            st.rerun()

    with action3:

        if st.button(
            "🏖️ Leave",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Leave"
            st.rerun()

    with action4:

        if st.button(
            "📊 Reports",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Reports"
            st.rerun()