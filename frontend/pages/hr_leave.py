import streamlit as st
from datetime import datetime

from api.client import api_request
from components.cards import section_header


def _status_badge(status):
    status = str(status or "Unknown").strip()

    styles = {
        "Pending": ("🟡", "Pending"),
        "Approved": ("🟢", "Approved"),
        "Rejected": ("🔴", "Rejected"),
    }

    icon, label = styles.get(status, ("⚪", status))
    return f"{icon} {label}"


def _format_date(value):
    if not value:
        return "—"

    try:
        if isinstance(value, str):
            return datetime.fromisoformat(value[:10]).strftime("%d %b %Y")
    except Exception:
        pass

    return str(value)


def _load_leave_data():
    dashboard, dashboard_error = api_request("GET", "/leave/dashboard")

    if dashboard_error:
        return None, dashboard_error

    requests_data, requests_error = api_request("GET", "/leave")

    if requests_error:
        return None, requests_error

    return {
        "dashboard": dashboard or {},
        "requests": requests_data or [],
    }, None


def show_hr_leave():
    st.markdown(
        """
        <style>
        .leave-hero {
            padding: 28px 30px;
            border-radius: 22px;
            background: linear-gradient(135deg, #172554 0%, #312e81 55%, #4f46e5 100%);
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 12px 35px rgba(49, 46, 129, 0.20);
        }

        .leave-hero h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 750;
        }

        .leave-hero p {
            margin: 8px 0 0 0;
            color: #dbeafe;
            font-size: 15px;
        }

        .leave-stat {
            padding: 20px;
            border-radius: 18px;
            background: white;
            border: 1px solid #e5e7eb;
            min-height: 125px;
        }

        .leave-stat-label {
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: .04em;
        }

        .leave-stat-value {
            font-size: 30px;
            font-weight: 750;
            color: #172033;
            margin-top: 8px;
        }

        .leave-stat-icon {
            font-size: 22px;
            float: right;
        }

        .request-card {
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #e5e7eb;
            background: #ffffff;
            margin-bottom: 12px;
        }

        .request-name {
            font-size: 17px;
            font-weight: 700;
            color: #172033;
        }

        .request-meta {
            color: #64748b;
            font-size: 13px;
            margin-top: 5px;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 650;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="leave-hero">
            <h1>🌿 Leave Management</h1>
            <p>
                Review employee leave requests, monitor approvals,
                and manage department leave activity.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data, error = _load_leave_data()

    if error:
        st.error(error)
        return

    dashboard = data["dashboard"]
    requests = data["requests"]

    summary = dashboard.get("summary", {})

    total = summary.get("total_requests", len(requests))
    pending = summary.get("pending", 0)
    approved = summary.get("approved", 0)
    rejected = summary.get("rejected", 0)

    # Overview

    cols = st.columns(4)

    stats = [
        ("Total Requests", total, "📋"),
        ("Pending", pending, "⏳"),
        ("Approved", approved, "✅"),
        ("Rejected", rejected, "❌"),
    ]

    for col, (label, value, icon) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="leave-stat">
                    <span class="leave-stat-icon">{icon}</span>
                    <div class="leave-stat-label">{label}</div>
                    <div class="leave-stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # Filters

    section_header(
        "Leave requests",
        "Filter requests and take action on pending applications.",
    )

    filter_col1, filter_col2, filter_col3 = st.columns([1, 1.5, 1])

    with filter_col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Pending", "Approved", "Rejected"],
        )

    with filter_col2:
        search = st.text_input(
            "Search employee",
            placeholder="Employee ID or employee name...",
        )

    with filter_col3:
        sort_option = st.selectbox(
            "Sort",
            ["Newest first", "Oldest first"],
        )

    filtered_requests = requests.copy()

    if status_filter != "All":
        filtered_requests = [
            request
            for request in filtered_requests
            if str(request.get("status", "")).strip().lower()
            == status_filter.lower()
        ]

    if search.strip():
        query = search.strip().lower()

        filtered_requests = [
            request
            for request in filtered_requests
            if query in str(request.get("employee_id", "")).lower()
            or query in str(request.get("employee_name", "")).lower()
            or query in str(request.get("first_name", "")).lower()
            or query in str(request.get("last_name", "")).lower()
        ]

    def date_value(request):
        value = request.get("created_at") or request.get("applied_at")

        if not value:
            return ""

        return str(value)

    filtered_requests.sort(
        key=date_value,
        reverse=sort_option == "Newest first",
    )

    st.caption(f"{len(filtered_requests)} request(s) found")

    if not filtered_requests:
        st.info("No leave requests match the selected filters.")
        return

    # Requests


    for request in filtered_requests:
        leave_id = request.get("leave_id", "—")
        employee_id = request.get("employee_id", "—")

        employee_name = (
            request.get("employee_name")
            or request.get("name")
            or "Employee"
        )

        if employee_name == "Employee":
            first_name = request.get("first_name", "")
            last_name = request.get("last_name", "")
            combined_name = f"{first_name} {last_name}".strip()

            if combined_name:
                employee_name = combined_name

        status = request.get("status", "Unknown")
        from_date = request.get("from_date")
        to_date = request.get("to_date")
        leave_days = request.get("leave_days", "—")
        reason = request.get("reason") or request.get("leave_reason") or "No reason provided"

        with st.container(border=True):
            top_left, top_right = st.columns([4, 1])

            with top_left:
                st.markdown(
                    f"### {employee_name}"
                )

                st.caption(
                    f"Employee ID: {employee_id}  •  "
                    f"Request #{leave_id}"
                )

            with top_right:
                st.markdown(
                    f"**{_status_badge(status)}**"
                )

            detail1, detail2, detail3 = st.columns(3)

            with detail1:
                st.caption("Leave period")
                st.write(
                    f"{_format_date(from_date)} → "
                    f"{_format_date(to_date)}"
                )

            with detail2:
                st.caption("Leave days")
                st.write(f"**{leave_days} day(s)**")

            with detail3:
                st.caption("Reason")
                st.write(reason)

            if str(status).lower() == "pending":
                st.divider()

                approve_col, reject_col, detail_col = st.columns(
                    [1, 1, 3]
                )

                with approve_col:
                    if st.button(
                        "✅ Approve",
                        key=f"approve_{leave_id}",
                        use_container_width=True,
                    ):
                        result, error = api_request(
                            "PUT",
                            f"/leave/approve/{leave_id}",
                        )

                        if error:
                            st.error(error)
                        else:
                            st.success("Leave request approved.")
                            st.rerun()

                with reject_col:
                    if st.button(
                        "❌ Reject",
                        key=f"reject_{leave_id}",
                        use_container_width=True,
                    ):
                        result, error = api_request(
                            "PUT",
                            f"/leave/reject/{leave_id}",
                        )

                        if error:
                            st.error(error)
                        else:
                            st.success("Leave request rejected.")
                            st.rerun()

                with detail_col:
                    st.caption(
                        "Pending requests can be approved or rejected."
                    )

    
    # Department summary
    

    st.write("")
    section_header(
        "Leave activity",
        "Summary returned by the HR leave dashboard API.",
    )

    activity_col1, activity_col2 = st.columns([1, 1])

    with activity_col1:
        approved_days = summary.get("approved_leave_days", 0)

        st.metric(
            "Approved leave days",
            approved_days,
        )

    with activity_col2:
        pending_ratio = (
            round((pending / total) * 100, 1)
            if total
            else 0
        )

        st.metric(
            "Pending request rate",
            f"{pending_ratio}%",
        )