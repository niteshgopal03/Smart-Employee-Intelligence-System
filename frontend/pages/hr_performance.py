import streamlit as st

from api.client import api_request
from components.cards import section_header


def _employee_label(employee):
    first = employee.get("first_name", "")
    last = employee.get("last_name", "")
    name = f"{first} {last}".strip()

    if not name:
        name = employee.get("employee_id", "Unknown Employee")

    return f"{name} • {employee.get('employee_id', '—')}"


def show_hr_performance():
    st.markdown(
        """
        <style>
        .performance-hero {
            padding: 30px;
            border-radius: 22px;
            background: linear-gradient(
                135deg,
                #581c87 0%,
                #7e22ce 52%,
                #a855f7 100%
            );
            color: white;
            margin-bottom: 25px;
            box-shadow: 0 14px 38px rgba(126, 34, 206, 0.22);
        }

        .performance-hero h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 750;
        }

        .performance-hero p {
            margin: 8px 0 0;
            color: #f3e8ff;
            font-size: 15px;
        }

        .rating-box {
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #e9d5ff;
            background: linear-gradient(
                145deg,
                #ffffff,
                #faf5ff
            );
        }

        .rating-number {
            font-size: 38px;
            font-weight: 800;
            color: #7e22ce;
        }

        .rating-label {
            color: #6b7280;
            font-size: 13px;
            font-weight: 600;
        }

        .info-box {
            padding: 16px 18px;
            border-radius: 14px;
            background: #faf5ff;
            border: 1px solid #e9d5ff;
            color: #581c87;
            margin-bottom: 18px;
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
        <div class="performance-hero">
            <h1>⭐ Performance Management</h1>
            <p>
                Review employee performance and maintain manager ratings
                used by the employee intelligence system.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Load employees
    # ---------------------------------------------------------

    employees, error = api_request("GET", "/employees")

    if error:
        st.error(error)
        return

    if not employees:
        st.info("No employees are available.")
        return

    # ---------------------------------------------------------
    # Employee selection
    # ---------------------------------------------------------

    section_header(
        "Select employee",
        "Choose an employee to view or update their manager rating.",
    )

    employee_options = {
        _employee_label(employee): employee
        for employee in employees
    }

    selected_label = st.selectbox(
        "Employee",
        list(employee_options.keys()),
    )

    selected_employee = employee_options[selected_label]
    employee_id = selected_employee.get("employee_id")

    if not employee_id:
        st.error("Selected employee does not have a valid employee ID.")
        return

    # ---------------------------------------------------------
    # Employee information
    # ---------------------------------------------------------

    first_name = selected_employee.get("first_name", "")
    last_name = selected_employee.get("last_name", "")
    name = f"{first_name} {last_name}".strip() or "Employee"

    department = (
        selected_employee.get("department_name")
        or selected_employee.get("department")
        or "—"
    )

    designation = selected_employee.get("designation") or "—"

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.caption("Employee")
        st.write(f"**{name}**")

    with info_col2:
        st.caption("Department")
        st.write(f"**{department}**")

    with info_col3:
        st.caption("Designation")
        st.write(f"**{designation}**")

    st.write("")

    # ---------------------------------------------------------
    # Load current performance
    # ---------------------------------------------------------

    performance, performance_error = api_request(
        "GET",
        f"/performance/{employee_id}",
    )

    if performance_error:
        st.warning(
            f"Could not load the current performance rating: "
            f"{performance_error}"
        )
        performance = {}

    current_rating = performance.get("manager_rating")

    # ---------------------------------------------------------
    # Current rating
    # ---------------------------------------------------------

    rating_col1, rating_col2 = st.columns([1, 2])

    with rating_col1:
        display_rating = (
            f"{float(current_rating):.1f}/5"
            if current_rating is not None
            else "Not rated"
        )

        st.markdown(
            f"""
            <div class="rating-box">
                <div class="rating-label">
                    CURRENT MANAGER RATING
                </div>
                <div class="rating-number">
                    {display_rating}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rating_col2:
        st.markdown(
            """
            <div class="info-box">
                <strong>How performance rating works</strong><br><br>
                Rate the employee from <strong>0.0 to 5.0</strong>.
                This manager rating is stored with the employee and can
                also be used by the AI prediction features.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # ---------------------------------------------------------
    # Update rating
    # ---------------------------------------------------------

    section_header(
        "Update performance rating",
        "Enter the latest manager assessment for this employee.",
    )

    default_rating = 0.0

    if current_rating is not None:
        try:
            default_rating = float(current_rating)
        except (TypeError, ValueError):
            default_rating = 0.0

    new_rating = st.slider(
        "Manager rating",
        min_value=0.0,
        max_value=5.0,
        value=default_rating,
        step=0.1,
        help="Rate the employee from 0.0 to 5.0.",
    )

    st.write(
        f"Selected rating: **{new_rating:.1f} / 5.0**"
    )

    save_col, reset_col = st.columns([1, 4])

    with save_col:
        save_rating = st.button(
            "💾 Save Rating",
            type="primary",
            use_container_width=True,
        )

   
    if save_rating:
        payload = {
            "manager_rating": round(new_rating, 1)
        }

        result, save_error = api_request(
            "PUT",
            f"/performance/{employee_id}",
            json=payload,
        )

        if save_error:
            st.error(save_error)
        else:
            st.success(
                f"Performance rating for {name} updated to "
                f"{new_rating:.1f}/5.0."
            )
            st.rerun()