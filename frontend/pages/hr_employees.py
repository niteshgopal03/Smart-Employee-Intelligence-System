import streamlit as st

from api.client import api_request
from components.cards import metric_card, section_header


def show_hr_employees():
    # ---------------------------------------------------------
    # Page Header
    # ---------------------------------------------------------
    st.title("Employee Directory")
    st.caption("HUMAN RESOURCES")
    st.write("Manage employees within your department.")
    st.divider()

    # ---------------------------------------------------------
    # Load Employees
    # ---------------------------------------------------------
    employees, error = api_request("GET", "/employees")

    if error:
        st.error(f"Unable to load employees: {error}")
        return

    if not isinstance(employees, list):
        employees = employees.get("employees", []) if isinstance(employees, dict) else []

    # ---------------------------------------------------------
    # Workforce Metrics
    # ---------------------------------------------------------
    total_employees = len(employees)

    active_employees = sum(
        1
        for employee in employees
        if str(employee.get("status", "")).lower() == "active"
    )

    inactive_employees = total_employees - active_employees

    departments = {
        employee.get("department")
        or employee.get("department_name")
        for employee in employees
        if employee.get("department") or employee.get("department_name")
    }

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Total Employees",
            total_employees,
            "Your department",
            "👥",
        )

    with col2:
        metric_card(
            "Active",
            active_employees,
            "Currently active",
            "🟢",
        )

    with col3:
        metric_card(
            "Inactive",
            inactive_employees,
            "Inactive / resigned",
            "⚪",
        )

    with col4:
        metric_card(
            "Department",
            len(departments),
            "Visible scope",
            "🏢",
        )

    st.write("")

    # ---------------------------------------------------------
    # Search + Add
    # ---------------------------------------------------------
    left, right = st.columns([4, 1])

    with left:
        search_text = st.text_input(
            "Search employees",
            placeholder="Search by employee ID, name, email or designation...",
            label_visibility="collapsed",
        )

    with right:
        add_clicked = st.button(
            "➕ Add Employee",
            type="primary",
            use_container_width=True,
        )

    # ---------------------------------------------------------
    # Add Employee Form
    # ---------------------------------------------------------
    if add_clicked:
        st.session_state["show_hr_add_employee"] = True

    if st.session_state.get("show_hr_add_employee", False):
        with st.container(border=True):
            section_header(
                "Add New Employee",
                "Create an employee inside your HR department.",
            )

            with st.form("add_employee_form"):
                c1, c2 = st.columns(2)

                with c1:
                    employee_id = st.text_input(
                        "Employee ID",
                        placeholder="EMP1005",
                    )

                    first_name = st.text_input(
                        "First Name",
                        placeholder="Aaryan",
                    )

                    last_name = st.text_input(
                        "Last Name",
                        placeholder="Sharma",
                    )

                    email = st.text_input(
                        "Email",
                        placeholder="employee@example.com",
                    )

                    phone = st.text_input(
                        "Phone",
                        placeholder="9876543210",
                    )

                with c2:
                    designation = st.text_input(
                        "Designation",
                        placeholder="Software Engineer",
                    )

                    education = st.text_input(
                        "Education",
                        placeholder="B.Tech",
                    )

                    skills = st.text_input(
                        "Skills",
                        placeholder="Python, SQL, FastAPI",
                    )

                    joining_date = st.date_input(
                        "Joining Date",
                    )

                    status = st.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                    )

                submitted = st.form_submit_button(
                    "Create Employee",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:
                    if not employee_id.strip():
                        st.error("Employee ID is required.")

                    elif not first_name.strip():
                        st.error("First name is required.")

                    elif not last_name.strip():
                        st.error("Last name is required.")

                    elif not email.strip():
                        st.error("Email is required.")

                    else:
                        payload = {
                            "employee_id": employee_id.strip(),
                            "first_name": first_name.strip(),
                            "last_name": last_name.strip(),
                            "email": email.strip(),
                            "phone": phone.strip(),
                            "designation": designation.strip(),
                            "education": education.strip(),
                            "skills": skills.strip(),
                            "joining_date": str(joining_date),
                            "status": status,
                        }

                        result, add_error = api_request(
                            "POST",
                            "/employee/add",
                            json=payload,
                        )

                        if add_error:
                            st.error(add_error)
                        else:
                            st.success("Employee created successfully.")
                            st.session_state["show_hr_add_employee"] = False
                            st.rerun()

            if st.button("Cancel", key="cancel_add_employee"):
                st.session_state["show_hr_add_employee"] = False
                st.rerun()

        st.write("")

    # ---------------------------------------------------------
    # Search Filtering
    # ---------------------------------------------------------
    if search_text.strip():
        search_response, search_error = api_request(
            "GET",
            "/employees/search",
            params={"search": search_text.strip()},
        )

        if not search_error and isinstance(search_response, list):
            employees = search_response
        elif not search_error and isinstance(search_response, dict):
            employees = search_response.get("employees", [])

    # ---------------------------------------------------------
    # Employee Directory
    # ---------------------------------------------------------
    section_header(
        "Employee Directory",
        f"{len(employees)} employee(s) visible in your department.",
    )

    if not employees:
        with st.container(border=True):
            st.info("No employees found.")
        return

    # ---------------------------------------------------------
    # Employee Cards
    # ---------------------------------------------------------
    for employee in employees:

        employee_id = employee.get("employee_id", "—")

        first_name = employee.get("first_name", "")
        last_name = employee.get("last_name", "")

        full_name = f"{first_name} {last_name}".strip() or "Unknown Employee"

        email = employee.get("email", "—")
        phone = employee.get("phone", "—")

        designation = employee.get("designation", "—")

        department = (
            employee.get("department")
            or employee.get("department_name")
            or "—"
        )

        status = employee.get("status", "—")

        with st.container(border=True):

            top_left, top_middle, top_right = st.columns([3, 3, 1])

            with top_left:
                st.markdown(f"### 👤 {full_name}")
                st.caption(f"Employee ID: **{employee_id}**")

            with top_middle:
                st.write(f"**{designation}**")
                st.caption(f"🏢 {department}")

            with top_right:
                if str(status).lower() == "active":
                    st.success("Active")
                else:
                    st.warning(str(status))

            st.divider()

            info1, info2, info3 = st.columns(3)

            with info1:
                st.caption("EMAIL")
                st.write(email)

            with info2:
                st.caption("PHONE")
                st.write(phone)

            with info3:
                st.caption("STATUS")
                st.write(status)

            st.write("")

            action1, action2, action3, spacer = st.columns(
                [1, 1, 1, 3]
            )

            # -------------------------------------------------
            # View
            # -------------------------------------------------
            with action1:
                if st.button(
                    "👁️ View",
                    key=f"view_{employee_id}",
                    use_container_width=True,
                ):
                    st.session_state["selected_employee"] = employee_id

            # -------------------------------------------------
            # Edit
            # -------------------------------------------------
            with action2:
                if st.button(
                    "✏️ Edit",
                    key=f"edit_{employee_id}",
                    use_container_width=True,
                ):
                    st.session_state["edit_employee"] = employee_id

            # -------------------------------------------------
            # Delete
            # -------------------------------------------------
            with action3:
                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{employee_id}",
                    use_container_width=True,
                ):
                    st.session_state["delete_employee"] = employee_id

    # ---------------------------------------------------------
    # View Employee
    # ---------------------------------------------------------
    selected_employee = st.session_state.get("selected_employee")

    if selected_employee:

        st.write("")

        employee_data, employee_error = api_request(
            "GET",
            f"/employee/{selected_employee}",
        )

        if employee_error:
            st.error(employee_error)
        else:
            with st.container(border=True):
                section_header(
                    "Employee Details",
                    f"Employee ID: {selected_employee}",
                )

                if isinstance(employee_data, dict):

                    details1, details2 = st.columns(2)

                    with details1:
                        st.write(
                            f"**Name:** "
                            f"{employee_data.get('first_name', '')} "
                            f"{employee_data.get('last_name', '')}"
                        )

                        st.write(
                            f"**Email:** "
                            f"{employee_data.get('email', '—')}"
                        )

                        st.write(
                            f"**Phone:** "
                            f"{employee_data.get('phone', '—')}"
                        )

                        st.write(
                            f"**Gender:** "
                            f"{employee_data.get('gender', '—')}"
                        )

                    with details2:
                        st.write(
                            f"**Designation:** "
                            f"{employee_data.get('designation', '—')}"
                        )

                        st.write(
                            f"**Department:** "
                            f"{employee_data.get('department_name', employee_data.get('department', '—'))}"
                        )

                        st.write(
                            f"**Education:** "
                            f"{employee_data.get('education', '—')}"
                        )

                        st.write(
                            f"**Skills:** "
                            f"{employee_data.get('skills', '—')}"
                        )

                if st.button(
                    "Close Details",
                    key="close_employee_details",
                ):
                    st.session_state["selected_employee"] = None
                    st.rerun()

    # ---------------------------------------------------------
    # Delete Confirmation
    # ---------------------------------------------------------
    delete_employee = st.session_state.get("delete_employee")

    if delete_employee:

        st.write("")

        with st.container(border=True):

            st.warning(
                f"Are you sure you want to delete employee "
                f"**{delete_employee}**?"
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:
                if st.button(
                    "Yes, Delete",
                    type="primary",
                    use_container_width=True,
                    key="confirm_delete_employee",
                ):
                    _, delete_error = api_request(
                        "DELETE",
                        f"/employee/delete/{delete_employee}",
                    )

                    if delete_error:
                        st.error(delete_error)
                    else:
                        st.success("Employee deleted successfully.")
                        st.session_state["delete_employee"] = None
                        st.rerun()

            with cancel_col:
                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key="cancel_delete_employee",
                ):
                    st.session_state["delete_employee"] = None
                    st.rerun()

    # ---------------------------------------------------------
    # Edit Employee
    # ---------------------------------------------------------
    edit_employee = st.session_state.get("edit_employee")

    if edit_employee:

        edit_data, edit_error = api_request(
            "GET",
            f"/employee/{edit_employee}",
        )

        if edit_error:
            st.error(edit_error)
        elif isinstance(edit_data, dict):

            st.write("")

            with st.container(border=True):

                section_header(
                    "Edit Employee",
                    f"Updating employee {edit_employee}",
                )

                with st.form(f"edit_employee_form_{edit_employee}"):

                    c1, c2 = st.columns(2)

                    with c1:
                        edit_first_name = st.text_input(
                            "First Name",
                            value=edit_data.get("first_name", ""),
                        )

                        edit_last_name = st.text_input(
                            "Last Name",
                            value=edit_data.get("last_name", ""),
                        )

                        edit_email = st.text_input(
                            "Email",
                            value=edit_data.get("email", ""),
                        )

                        edit_phone = st.text_input(
                            "Phone",
                            value=edit_data.get("phone", ""),
                        )

                    with c2:
                        edit_designation = st.text_input(
                            "Designation",
                            value=edit_data.get("designation", ""),
                        )

                        edit_education = st.text_input(
                            "Education",
                            value=edit_data.get("education", ""),
                        )

                        edit_skills = st.text_input(
                            "Skills",
                            value=edit_data.get("skills", ""),
                        )

                        edit_status = st.selectbox(
                            "Status",
                            ["Active", "Inactive", "Resigned"],
                            index=(
                                ["Active", "Inactive", "Resigned"].index(
                                    edit_data.get("status", "Active")
                                )
                                if edit_data.get("status", "Active")
                                in ["Active", "Inactive", "Resigned"]
                                else 0
                            ),
                        )

                    save_changes = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True,
                    )

                    if save_changes:

                        payload = {
                            **edit_data,
                            "first_name": edit_first_name.strip(),
                            "last_name": edit_last_name.strip(),
                            "email": edit_email.strip(),
                            "phone": edit_phone.strip(),
                            "designation": edit_designation.strip(),
                            "education": edit_education.strip(),
                            "skills": edit_skills.strip(),
                            "status": edit_status,
                        }

                        _, update_error = api_request(
                            "PUT",
                            f"/employee/update/{edit_employee}",
                            json=payload,
                        )

                        if update_error:
                            st.error(update_error)
                        else:
                            st.success("Employee updated successfully.")
                            st.session_state["edit_employee"] = None
                            st.rerun()

                if st.button(
                    "Cancel Editing",
                    key=f"cancel_edit_{edit_employee}",
                ):
                    st.session_state["edit_employee"] = None
                    st.rerun()