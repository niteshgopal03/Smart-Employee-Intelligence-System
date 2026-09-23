import streamlit as st

from api.client import api_request


def show_employee_leave():

    st.title("🏖️ Leave Center")
    st.caption("Manage your leave balance and track your requests.")

    st.write("")

    # ---------------------------------------------------------
    # Load Leave Data
    # ---------------------------------------------------------

    data, error = api_request(
        "GET",
        "/employee/me/leave",
    )

    if error:
        st.error(error)
        return

    records = data

    if isinstance(data, dict):
        records = (
            data.get("leave_requests")
            or data.get("leave")
            or data.get("leaves")
            or data.get("data")
            or []
        )

    if not isinstance(records, list):
        records = []

    # ---------------------------------------------------------
    # Calculate Leave Summary
    # ---------------------------------------------------------

    total_requests = len(records)
    pending = 0
    approved = 0
    rejected = 0
    total_approved_days = 0

    for leave in records:

        status = str(
            leave.get("status", "")
        ).lower()

        if status == "pending":
            pending += 1

        elif status == "approved":
            approved += 1

            days = (
                leave.get("leave_days")
                or leave.get("days")
                or 0
            )

            try:
                total_approved_days += int(days)
            except (TypeError, ValueError):
                pass

        elif status == "rejected":
            rejected += 1

    # ---------------------------------------------------------
    # Leave Overview
    # ---------------------------------------------------------

    st.subheader("Leave Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.caption("TOTAL REQUESTS")
            st.markdown(f"## {total_requests}")
            st.caption("All submitted requests")

    with col2:
        with st.container(border=True):
            st.caption("PENDING")
            st.markdown(f"## {pending}")
            st.caption("Awaiting HR approval")

    with col3:
        with st.container(border=True):
            st.caption("APPROVED")
            st.markdown(f"## {approved}")
            st.caption("Approved requests")

    with col4:
        with st.container(border=True):
            st.caption("DAYS USED")
            st.markdown(f"## {total_approved_days}")
            st.caption("Approved leave days")

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # Apply for Leave
    # ---------------------------------------------------------

    st.subheader("Request Leave")
    st.caption("Submit a new leave request.")

    with st.container(border=True):

        leave_col1, leave_col2 = st.columns(2)

        with leave_col1:
            start_date = st.date_input(
                "Start Date",
                key="leave_start_date",
            )

        with leave_col2:
            end_date = st.date_input(
                "End Date",
                key="leave_end_date",
            )

        reason = st.text_area(
            "Reason",
            placeholder="Enter the reason for your leave...",
            height=110,
            key="leave_reason",
        )

        st.write("")

        if st.button(
            "📨 Submit Leave Request",
            type="primary",
            use_container_width=True,
        ):

            if end_date < start_date:
                st.error(
                    "End date cannot be before start date."
                )
                return

            if not reason.strip():
                st.warning(
                    "Please provide a reason for your leave."
                )
                return

            leave_data = {
                "from_date": str(start_date),
                "to_date": str(end_date),
                "reason": reason.strip(),
            }

            with st.spinner("Submitting leave request..."):

                result, submit_error = api_request(
                    "POST",
                    "/leave/apply",
                    json=leave_data,
                )

            if submit_error:
                st.error(submit_error)
                return

            message = (
                result.get(
                    "message",
                    "Leave request submitted successfully.",
                )
                if isinstance(result, dict)
                else "Leave request submitted successfully."
            )

            st.success(message)

            st.rerun()

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # Leave History
    # ---------------------------------------------------------

    st.subheader("Leave History")
    st.caption("Review your previously submitted leave requests.")

    if not records:

        with st.container(border=True):
            st.info(
                "You have not submitted any leave requests yet."
            )

        return

    display_records = []

    for leave in records:

        status = leave.get(
            "status",
            "—",
        )

        display_records.append(
            {
                "Start Date": (
                    leave.get("from_date")
                    or leave.get("start_date")
                    or "—"
                ),
                "End Date": (
                    leave.get("to_date")
                    or leave.get("end_date")
                    or "—"
                ),
                "Days": (
                    leave.get("leave_days")
                    or leave.get("days")
                    or "—"
                ),
                "Reason": (
                    leave.get("reason")
                    or "—"
                ),
                "Status": status,
            }
        )

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True,
    )