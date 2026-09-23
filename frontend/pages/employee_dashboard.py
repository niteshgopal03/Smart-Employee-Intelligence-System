from datetime import date

import streamlit as st

from api.client import api_request
from components.cards import metric_card, section_header


def show_employee_dashboard():

    st.title("Employee Dashboard")

    st.caption(
        f"Welcome back, {st.session_state.get('username', 'Employee')}."
    )

    st.write("")

    employee_id = st.session_state.get("employee_id")

   
    # Load real data from the backend.
    # Each call fails independently so one broken endpoint
    # doesn't take down the whole dashboard.
   

    percentage_data, percentage_error = api_request(
        "GET",
        "/attendance/my/percentage",
    )

    attendance_percentage = None

    if not percentage_error and isinstance(percentage_data, dict):
        attendance_percentage = (
            percentage_data.get("attendance_percentage")
            or percentage_data.get("percentage")
        )

    today = date.today()

    attendance_data, attendance_error = api_request(
        "GET",
        f"/employee/me/attendance?month={today.month}&year={today.year}",
    )

    attendance_records = []

    if not attendance_error:

        raw_records = attendance_data

        if isinstance(attendance_data, dict):
            raw_records = (
                attendance_data.get("attendance")
                or attendance_data.get("records")
                or attendance_data.get("data")
                or []
            )

        if isinstance(raw_records, list):
            attendance_records = raw_records

    leave_data, leave_error = api_request(
        "GET",
        "/employee/me/leave",
    )

    leave_records = []

    if not leave_error:

        raw_leave = leave_data

        if isinstance(leave_data, dict):
            raw_leave = (
                leave_data.get("leave_requests")
                or leave_data.get("leave")
                or leave_data.get("leaves")
                or leave_data.get("data")
                or []
            )

        if isinstance(raw_leave, list):
            leave_records = raw_leave

    pending_leave = 0
    approved_leave = 0

    for leave in leave_records:

        status = str(leave.get("status", "")).lower()

        if status == "pending":
            pending_leave += 1

        elif status == "approved":
            approved_leave += 1

    performance_data, performance_error = api_request(
        "GET",
        f"/performance/{employee_id}",
    ) if employee_id else (None, "Employee ID missing from session.")

    manager_rating = None

    if not performance_error and isinstance(performance_data, dict):

        raw_rating = performance_data.get("manager_rating")

        try:
            manager_rating = float(raw_rating) if raw_rating is not None else None
        except (TypeError, ValueError):
            manager_rating = None

    profile_data, profile_error = api_request(
        "GET",
        "/employee/me",
    )

    employment_status = "—"
    leave_balance = None

    if not profile_error and isinstance(profile_data, dict):
        employee = profile_data.get("employee", profile_data)
        employment_status = employee.get("status", "—")
        leave_balance = employee.get("leave_balance")

    # --------------------------------
    # Summary
    # --------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Attendance",
            f"{attendance_percentage}%" if attendance_percentage is not None else "—",
            "Overall attendance",
            "📅",
        )

    with col2:
        metric_card(
            "Leave Balance",
            f"{leave_balance} Days" if leave_balance is not None else "—",
            "Remaining",
            "🏖️",
        )

    with col3:
        metric_card(
            "Performance",
            f"{manager_rating:.1f}/5" if manager_rating is not None else "Not rated",
            "Manager rating",
            "📈",
        )

    with col4:
        metric_card(
            "Employment",
            employment_status,
            "Current status",
            "👤",
        )

    st.write("")

    # --------------------------------
    # Quick Actions
    # --------------------------------

    section_header(
        "Quick Actions",
        "Access your frequently used employee services.",
    )

    action1, action2, action3 = st.columns(3)

    with action1:

        if st.button(
            "📅 View Attendance",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Attendance"
            st.rerun()

    with action2:

        if st.button(
            "🏖️ Apply for Leave",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Leave"
            st.rerun()

    with action3:

        if st.button(
            "📊 View Performance",
            use_container_width=True,
        ):
            st.session_state["nav_target"] = "Performance"
            st.rerun()

    st.write("")

    # --------------------------------
    # Recent Activity
    # --------------------------------

    section_header(
        "Recent Activity",
        "A quick overview of your recent activity.",
    )

    activity_col, leave_col = st.columns([1.5, 1])

    # Recent attendance (real records, most recent first)
    with activity_col:

        with st.container(border=True):

            st.markdown("#### 📅 Recent Attendance")

            st.write("")

            if attendance_error:

                st.warning(attendance_error)

            elif not attendance_records:

                st.info("No attendance records found for this month yet.")

            else:

                def record_sort_key(record):
                    return (
                        record.get("attendance_date")
                        or record.get("date")
                        or ""
                    )

                sorted_records = sorted(
                    attendance_records,
                    key=record_sort_key,
                    reverse=True,
                )[:3]

                for index, record in enumerate(sorted_records):

                    record_date = (
                        record.get("attendance_date")
                        or record.get("date")
                        or "—"
                    )

                    status = str(
                        record.get("status", "—")
                    ).strip()

                    row1, row2 = st.columns([3, 1])

                    with row1:
                        st.write(record_date)

                    with row2:

                        status_lower = status.lower()

                        if status_lower == "present":
                            st.success(status)
                        elif status_lower == "absent":
                            st.error(status)
                        elif status_lower == "leave":
                            st.warning(status)
                        else:
                            st.info(status)

                    if index < len(sorted_records) - 1:
                        st.divider()

    # Leave status (real counts)
    with leave_col:

        with st.container(border=True):

            st.markdown("#### 🏖️ Leave Status")

            st.write("")

            if leave_error:

                st.warning(leave_error)

            else:

                st.metric(
                    "Pending Requests",
                    pending_leave,
                )

                st.divider()

                st.metric(
                    "Approved",
                    approved_leave,
                )

                st.divider()

                st.metric(
                    "Total Requests",
                    len(leave_records),
                )