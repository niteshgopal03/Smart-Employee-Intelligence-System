import calendar
from datetime import date

import streamlit as st

from api.client import api_request
from components.cards import metric_card, section_header


def show_hr_attendance():
   
    # Page Header
   
    st.caption("HUMAN RESOURCES")
    st.title("Attendance Control")
    st.caption("Monitor and manage attendance records for your department.")

   
    # Load Attendance
   
    attendance, error = api_request("GET", "/attendance")

    if error:
        st.error(f"Unable to load attendance records: {error}")
        return

    if not isinstance(attendance, list):
        attendance = (
            attendance.get("attendance", [])
            if isinstance(attendance, dict)
            else []
        )

   
    # Attendance Metrics
   
    total_records = len(attendance)

    present_count = sum(
        1
        for record in attendance
        if str(record.get("status", "")).lower() == "present"
    )

    absent_count = sum(
        1
        for record in attendance
        if str(record.get("status", "")).lower() == "absent"
    )

    leave_count = sum(
        1
        for record in attendance
        if str(record.get("status", "")).lower() == "leave"
    )

    attendance_percentage = (
        (present_count / total_records) * 100
        if total_records
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Attendance Rate",
            f"{attendance_percentage:.1f}%",
            "Department records",
            "📈",
        )

    with col2:
        metric_card(
            "Present",
            present_count,
            "Attendance marked",
            "🟢",
        )

    with col3:
        metric_card(
            "Absent",
            absent_count,
            "Absent records",
            "🔴",
        )

    with col4:
        metric_card(
            "Leave",
            leave_count,
            "Leave records",
            "🟡",
        )

    st.write("")

   
    # Controls
   
    control1, control2, control3 = st.columns([2, 2, 1])

    with control1:
        selected_month = st.selectbox(
            "Month",
            list(range(1, 13)),
            index=date.today().month - 1,
            format_func=lambda x: calendar.month_name[x],
        )

    with control2:
        selected_year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=date.today().year,
            step=1,
        )

    with control3:
        mark_clicked = st.button(
            "➕ Mark Attendance",
            type="primary",
            use_container_width=True,
        )

   
    # Mark Attendance
   
    if mark_clicked:
        st.session_state["show_mark_attendance"] = True

    if st.session_state.get("show_mark_attendance", False):

        st.write("")

        with st.container(border=True):

            section_header(
                "Mark Attendance",
                "Create an attendance record for an employee in your department.",
            )

            employee_options = sorted(
                {
                    record.get("employee_id")
                    for record in attendance
                    if record.get("employee_id")
                }
            )

            with st.form("mark_attendance_form"):

                c1, c2 = st.columns(2)

                with c1:
                    if employee_options:
                        employee_id = st.selectbox(
                            "Employee",
                            employee_options,
                        )
                    else:
                        employee_id = st.text_input(
                            "Employee ID",
                            placeholder="EMP1001",
                        )

                    attendance_date = st.date_input(
                        "Attendance Date",
                        value=date.today(),
                    )

                with c2:
                    status = st.selectbox(
                        "Status",
                        ["Present", "Absent", "Leave"],
                    )

                    check_in = st.time_input(
                        "Check In",
                    )

                    check_out = st.time_input(
                        "Check Out",
                    )

                submitted = st.form_submit_button(
                    "Save Attendance",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:

                    if not employee_id:
                        st.error("Employee ID is required.")

                    else:
                        payload = {
                            "employee_id": employee_id,
                            "attendance_date": str(attendance_date),
                            "check_in": (
                                check_in.strftime("%H:%M:%S")
                                if status == "Present"
                                else None
                            ),
                            "check_out": (
                                check_out.strftime("%H:%M:%S")
                                if status == "Present"
                                else None
                            ),
                            "status": status,
                        }

                        _, mark_error = api_request(
                            "POST",
                            "/attendance/mark",
                            json=payload,
                        )

                        if mark_error:
                            st.error(mark_error)
                        else:
                            st.success(
                                "Attendance marked successfully."
                            )
                            st.session_state[
                                "show_mark_attendance"
                            ] = False
                            st.rerun()

            if st.button(
                "Cancel",
                key="cancel_mark_attendance",
            ):
                st.session_state["show_mark_attendance"] = False
                st.rerun()

        st.write("")

   
    # Filter Records
   
    section_header(
        "Attendance Records",
        f"Records for {calendar.month_name[selected_month]} {selected_year}",
    )

    search_employee = st.text_input(
        "Employee filter",
        placeholder="Enter employee ID...",
        key="attendance_employee_search",
    )

    filtered_records = []

    for record in attendance:

        record_date = record.get(
            "attendance_date",
            record.get("date"),
        )

        if record_date:

            try:
                if hasattr(record_date, "month"):
                    record_month = record_date.month
                    record_year = record_date.year
                else:
                    parsed_date = date.fromisoformat(
                        str(record_date)[:10]
                    )
                    record_month = parsed_date.month
                    record_year = parsed_date.year

                if (
                    record_month != selected_month
                    or record_year != selected_year
                ):
                    continue

            except Exception:
                pass

        if search_employee.strip():

            record_employee = str(
                record.get("employee_id", "")
            ).lower()

            if search_employee.strip().lower() not in record_employee:
                continue

        filtered_records.append(record)

   
    # Records Table
   
    if not filtered_records:
        with st.container(border=True):
            st.info(
                "No attendance records found for the selected filters."
            )
    else:

        table_rows = []

        for record in filtered_records:

            table_rows.append(
                {
                    "Employee ID": record.get(
                        "employee_id",
                        "—",
                    ),
                    "Date": record.get(
                        "attendance_date",
                        record.get("date", "—"),
                    ),
                    "Check In": record.get(
                        "check_in",
                        "—",
                    ),
                    "Check Out": record.get(
                        "check_out",
                        "—",
                    ),
                    "Status": record.get(
                        "status",
                        "—",
                    ),
                }
            )

        st.dataframe(
            table_rows,
            use_container_width=True,
            hide_index=True,
        )

   
    # Attendance Calendar
   
    st.write("")

    section_header(
        "Attendance Calendar",
        "Monthly attendance distribution.",
    )

    month_records = []

    for record in filtered_records:
        record_date = record.get(
            "attendance_date",
            record.get("date"),
        )

        if record_date:
            month_records.append(record)

    if month_records:

        calendar_days = []

        for record in month_records:

            record_date = record.get(
                "attendance_date",
                record.get("date"),
            )

            status = str(
                record.get("status", "")
            ).lower()

            calendar_days.append(
                {
                    "Date": str(record_date),
                    "Employee": record.get(
                        "employee_id",
                        "—",
                    ),
                    "Status": status.title(),
                }
            )

        st.dataframe(
            calendar_days,
            use_container_width=True,
            hide_index=True,
        )

   
    # Update Attendance
   
    st.write("")

    section_header(
        "Update Attendance",
        "Modify an existing attendance record.",
    )

    attendance_ids = [
        record.get("attendance_id")
        for record in filtered_records
        if record.get("attendance_id") is not None
    ]

    if not attendance_ids:
        st.info(
            "No attendance IDs are available for editing."
        )
        return

    selected_attendance_id = st.selectbox(
        "Attendance Record",
        attendance_ids,
        key="selected_attendance_id",
    )

    selected_record = next(
        (
            record
            for record in filtered_records
            if record.get("attendance_id")
            == selected_attendance_id
        ),
        None,
    )

    if selected_record:

        with st.container(border=True):

            with st.form(
                f"update_attendance_{selected_attendance_id}"
            ):

                status_options = [
                    "Present",
                    "Absent",
                    "Leave",
                ]

                current_status = selected_record.get(
                    "status",
                    "Present",
                )

                status_index = (
                    status_options.index(current_status)
                    if current_status in status_options
                    else 0
                )

                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_index,
                )

                new_check_in = st.text_input(
                    "Check In",
                    value=str(
                        selected_record.get(
                            "check_in",
                            "",
                        )
                    ),
                )

                new_check_out = st.text_input(
                    "Check Out",
                    value=str(
                        selected_record.get(
                            "check_out",
                            "",
                        )
                    ),
                )

                update_clicked = st.form_submit_button(
                    "💾 Update Attendance",
                    type="primary",
                    use_container_width=True,
                )

                if update_clicked:

                    payload = {
                        "employee_id": selected_record.get(
                            "employee_id"
                        ),
                        "attendance_date": selected_record.get(
                            "attendance_date",
                            selected_record.get("date"),
                        ),
                        "check_in": (
                            new_check_in
                            if new_status == "Present"
                            else None
                        ),
                        "check_out": (
                            new_check_out
                            if new_status == "Present"
                            else None
                        ),
                        "status": new_status,
                    }

                    _, update_error = api_request(
                        "PUT",
                        f"/attendance/update/{selected_attendance_id}",
                        json=payload,
                    )

                    if update_error:
                        st.error(update_error)
                    else:
                        st.success(
                            "Attendance updated successfully."
                        )
                        st.rerun()