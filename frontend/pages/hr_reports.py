import streamlit as st
import pandas as pd

from api.client import api_request
from components.cards import section_header


def _get_report(endpoint):
    data, error = api_request("GET", endpoint)

    if error:
        st.error(error)
        return None

    return data or {}


def _metric_card(title, value, icon):
    st.markdown(
        f"""
        <div style="
            padding:18px 20px;
            border:1px solid #e5e7eb;
            border-radius:16px;
            background:linear-gradient(145deg,#ffffff,#f8fafc);
            min-height:115px;
        ">
            <div style="font-size:24px;">{icon}</div>
            <div style="
                color:#64748b;
                font-size:12px;
                font-weight:700;
                text-transform:uppercase;
                margin-top:7px;
            ">{title}</div>
            <div style="
                color:#172033;
                font-size:27px;
                font-weight:750;
                margin-top:5px;
            ">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_hr_reports():
    st.markdown(
        """
        <style>
        .reports-hero {
            padding:30px;
            border-radius:22px;
            background:
                linear-gradient(
                    135deg,
                    #064e3b 0%,
                    #047857 50%,
                    #0f766e 100%
                );
            color:white;
            margin-bottom:25px;
            box-shadow:0 14px 38px rgba(4,120,87,.20);
        }

        .reports-hero h1 {
            margin:0;
            font-size:32px;
            font-weight:750;
        }

        .reports-hero p {
            margin:8px 0 0;
            color:#d1fae5;
            font-size:15px;
        }

        .report-section {
            padding:18px 20px;
            border-radius:16px;
            background:#f8fafc;
            border:1px solid #e2e8f0;
        }

        .stButton > button {
            border-radius:10px;
            font-weight:650;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="reports-hero">
            <h1>📊 HR Reports & Analytics</h1>
            <p>
                Explore workforce, attendance, leave, performance,
                salary and department-level insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

   
    # Report selector
   

    report_type = st.selectbox(
        "Select report",
        [
            "Employee Overview",
            "Department Overview",
            "Attendance",
            "Leave",
            "Performance",
            "Salary",
        ],
    )

    st.write("")


    # Employee report
    
    if report_type == "Employee Overview":
        data = _get_report("/hr/reports/employees")

        if data is None:
            return

        total = data.get("total_employees", 0)
        active = data.get("active_employees", 0)
        resigned = data.get("resigned_employees", 0)

        c1, c2, c3 = st.columns(3)

        with c1:
            _metric_card("Total employees", total, "👥")

        with c2:
            _metric_card("Active employees", active, "🟢")

        with c3:
            _metric_card("Resigned employees", resigned, "⚪")

        st.write("")
        section_header(
            "Workforce overview",
            "Current employee status summary.",
        )

        df = pd.DataFrame(
            [
                {
                    "Category": "Active",
                    "Employees": active,
                },
                {
                    "Category": "Resigned",
                    "Employees": resigned,
                },
            ]
        )

        st.bar_chart(
            df.set_index("Category"),
            use_container_width=True,
        )

    
    # Department report
    
    elif report_type == "Department Overview":
        data = _get_report("/hr/reports/departments")

        if data is None:
            return

        departments = data.get("departments", [])

        section_header(
            "Department distribution",
            "Employee distribution across your accessible departments.",
        )

        if not departments:
            st.info("No department data available.")
            return

        df = pd.DataFrame(departments)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        possible_name_columns = [
            "department_name",
            "name",
            "department",
        ]

        possible_count_columns = [
            "employee_count",
            "employees",
            "count",
        ]

        name_col = next(
            (c for c in possible_name_columns if c in df.columns),
            None,
        )

        count_col = next(
            (c for c in possible_count_columns if c in df.columns),
            None,
        )

        if name_col and count_col:
            chart_df = df[[name_col, count_col]].copy()
            chart_df.columns = ["Department", "Employees"]

            st.bar_chart(
                chart_df.set_index("Department"),
                use_container_width=True,
            )

    
    # Attendance report

    elif report_type == "Attendance":
        data = _get_report("/hr/reports/attendance")

        if data is None:
            return

        total = data.get("total_records", 0)
        present = data.get("present", 0)
        absent = data.get("absent", 0)
        leave = data.get("leave", 0)
        percentage = data.get("attendance_percentage", 0)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            _metric_card("Total records", total, "📋")

        with c2:
            _metric_card("Present", present, "🟢")

        with c3:
            _metric_card("Absent", absent, "🔴")

        with c4:
            _metric_card("Leave", leave, "🟡")

        st.write("")

        st.metric(
            "Attendance percentage",
            f"{percentage}%",
        )

        st.write("")

        chart_df = pd.DataFrame(
            {
                "Status": ["Present", "Absent", "Leave"],
                "Records": [present, absent, leave],
            }
        )

        st.bar_chart(
            chart_df.set_index("Status"),
            use_container_width=True,
        )

    
    # Leave report

    elif report_type == "Leave":
        data = _get_report("/hr/reports/leave")

        if data is None:
            return

        total = data.get("total_requests", 0)
        pending = data.get("pending", 0)
        approved = data.get("approved", 0)
        rejected = data.get("rejected", 0)
        approved_days = data.get("approved_leave_days", 0)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            _metric_card("Total requests", total, "📋")

        with c2:
            _metric_card("Pending", pending, "⏳")

        with c3:
            _metric_card("Approved", approved, "✅")

        with c4:
            _metric_card("Rejected", rejected, "❌")

        st.write("")

        st.metric(
            "Approved leave days",
            approved_days,
        )

        chart_df = pd.DataFrame(
            {
                "Status": [
                    "Pending",
                    "Approved",
                    "Rejected",
                ],
                "Requests": [
                    pending,
                    approved,
                    rejected,
                ],
            }
        )

        st.bar_chart(
            chart_df.set_index("Status"),
            use_container_width=True,
        )


    # Performance report

    elif report_type == "Performance":
        data = _get_report("/hr/reports/performance")

        if data is None:
            return

        summary = data.get("summary", data)

        rated = summary.get("rated_employees", 0)
        average = summary.get("average_rating", 0)
        highest = summary.get("highest_rating", 0)
        lowest = summary.get("lowest_rating", 0)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            _metric_card("Rated employees", rated, "👤")

        with c2:
            _metric_card("Average rating", average, "⭐")

        with c3:
            _metric_card("Highest rating", highest, "🏆")

        with c4:
            _metric_card("Lowest rating", lowest, "📉")

        st.write("")

        rating_df = pd.DataFrame(
            {
                "Metric": [
                    "Average",
                    "Highest",
                    "Lowest",
                ],
                "Rating": [
                    average,
                    highest,
                    lowest,
                ],
            }
        )

        st.bar_chart(
            rating_df.set_index("Metric"),
            use_container_width=True,
        )


    # Salary report

    elif report_type == "Salary":
        data = _get_report("/hr/reports/salary")

        if data is None:
            return

        summary = data.get("summary", data)

        employees = summary.get("employees_with_salary", 0)
        average = summary.get("average_salary", 0)
        minimum = summary.get("minimum_salary", 0)
        maximum = summary.get("maximum_salary", 0)
        total = summary.get("total_salary", 0)

        c1, c2, c3 = st.columns(3)

        with c1:
            _metric_card(
                "Employees with salary",
                employees,
                "👥",
            )

        with c2:
            _metric_card(
                "Average salary",
                f"₹{average:,.0f}",
                "💰",
            )

        with c3:
            _metric_card(
                "Total salary",
                f"₹{total:,.0f}",
                "💳",
            )

        st.write("")

        c4, c5 = st.columns(2)

        with c4:
            st.metric(
                "Minimum salary",
                f"₹{minimum:,.0f}",
            )

        with c5:
            st.metric(
                "Maximum salary",
                f"₹{maximum:,.0f}",
            )

        st.write("")

        salary_df = pd.DataFrame(
            {
                "Metric": [
                    "Minimum",
                    "Average",
                    "Maximum",
                ],
                "Salary": [
                    minimum,
                    average,
                    maximum,
                ],
            }
        )

        st.bar_chart(
            salary_df.set_index("Metric"),
            use_container_width=True,
        )