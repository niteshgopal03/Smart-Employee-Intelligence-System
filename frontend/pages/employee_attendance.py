import calendar
from datetime import date

import streamlit as st

from api.client import api_request


def show_employee_attendance():

    st.title("📊 My Attendance")
    st.caption("Track your attendance, working days, and monthly presence.")

    st.write("")

    # ---------------------------------------------------------
    # Load Attendance Percentage
    # ---------------------------------------------------------

    percentage_data, percentage_error = api_request(
        "GET",
        "/attendance/my/percentage",
    )

    if percentage_error:
        st.error(percentage_error)
        return

    attendance_percentage = 0

    if isinstance(percentage_data, dict):
        attendance_percentage = (
            percentage_data.get("attendance_percentage")
            or percentage_data.get("percentage")
            or 0
        )

    # ---------------------------------------------------------
    # Top Summary
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns([1.3, 1, 1])

    with col1:
        with st.container(border=True):
            st.caption("ATTENDANCE SCORE")
            st.markdown(
                f"## {attendance_percentage}%"
            )
            st.progress(
                min(float(attendance_percentage) / 100, 1.0)
            )
            st.caption("Overall attendance percentage")

    with col2:
        with st.container(border=True):
            st.caption("EMPLOYEE")
            st.markdown(
                f"### {st.session_state.get('employee_id', '—')}"
            )
            st.caption("Currently logged in")

    with col3:
        with st.container(border=True):
            st.caption("TODAY")
            st.markdown(
                f"### {date.today().strftime('%d %b')}"
            )
            st.caption(
                date.today().strftime("%A")
            )

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # Month Selector
    # ---------------------------------------------------------

    st.subheader("Monthly Attendance")
    st.caption("Select a month to view your detailed attendance.")

    month_col, year_col, button_col = st.columns([1, 1, 1.2])

    today = date.today()

    with month_col:
        selected_month = st.selectbox(
            "Month",
            range(1, 13),
            index=today.month - 1,
            format_func=lambda x: calendar.month_name[x],
        )

    with year_col:
        selected_year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=today.year,
            step=1,
        )

    with button_col:
        st.write("")
        load_clicked = st.button(
            "🔎 View Attendance",
            type="primary",
            use_container_width=True,
        )

    # Automatically load current month initially
    if "attendance_loaded" not in st.session_state:
        st.session_state.attendance_loaded = True
        st.session_state.attendance_month = today.month
        st.session_state.attendance_year = today.year

    if load_clicked:
        st.session_state.attendance_month = selected_month
        st.session_state.attendance_year = selected_year

    month = st.session_state.attendance_month
    year = st.session_state.attendance_year

    st.write("")

    # ---------------------------------------------------------
    # Monthly API
    # ---------------------------------------------------------

    attendance_data, attendance_error = api_request(
        "GET",
        f"/employee/me/attendance?month={month}&year={year}",
    )

    if attendance_error:
        st.error(attendance_error)
        return

    records = attendance_data

    if isinstance(attendance_data, dict):
        records = (
            attendance_data.get("attendance")
            or attendance_data.get("records")
            or attendance_data.get("data")
            or []
        )

    if not isinstance(records, list):
        records = []

    # ---------------------------------------------------------
    # Calculate Summary
    # ---------------------------------------------------------

    present_count = 0
    absent_count = 0
    leave_count = 0

    for record in records:

        status = str(
            record.get("status", "")
        ).lower()

        if status == "present":
            present_count += 1

        elif status == "absent":
            absent_count += 1

        elif status == "leave":
            leave_count += 1

    total_days = len(records)

    # ---------------------------------------------------------
    # Monthly Statistics
    # ---------------------------------------------------------

    st.subheader(
        f"{calendar.month_name[month]} {year}"
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        with st.container(border=True):
            st.metric(
                "Present",
                present_count,
            )

    with stat2:
        with st.container(border=True):
            st.metric(
                "Absent",
                absent_count,
            )

    with stat3:
        with st.container(border=True):
            st.metric(
                "Leave",
                leave_count,
            )

    with stat4:
        with st.container(border=True):
            st.metric(
                "Recorded Days",
                total_days,
            )

    st.write("")

    # ---------------------------------------------------------
    # Attendance Records
    # ---------------------------------------------------------

    st.subheader("Attendance History")

    if not records:
        with st.container(border=True):
            st.info(
                "No attendance records found for the selected month."
            )
        return

    display_records = []

    for record in records:

        attendance_date = (
            record.get("attendance_date")
            or record.get("date")
            or "—"
        )

        status = record.get(
            "status",
            "—",
        )

        check_in = (
            record.get("check_in")
            or record.get("in_time")
            or "—"
        )

        check_out = (
            record.get("check_out")
            or record.get("out_time")
            or "—"
        )

        display_records.append(
            {
                "Date": attendance_date,
                "Status": status,
                "Check In": check_in,
                "Check Out": check_out,
            }
        )

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True,
    )