import streamlit as st

from api.client import api_request


def show_admin_hr():
    st.title("👥 HR Management") 
    st.caption("Manage HR accounts and department assignments.")


    data, error = api_request("GET", "/admin/hr")

    if error:
        st.error(error)
        return

    hr_list = data.get("hr", []) if isinstance(data, dict) else []

    # ---------------------------------------------------------
    # TOP METRICS
    # ---------------------------------------------------------
    total_hr = len(hr_list)

    active_hr = sum(
        1
        for hr in hr_list
        if str(hr.get("status", "")).lower() == "active"
    )

    inactive_hr = total_hr - active_hr

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total HR", total_hr)

    with col2:
        st.metric("Active HR", active_hr)

    with col3:
        st.metric("Inactive HR", inactive_hr)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ADD HR BUTTON
    # ---------------------------------------------------------
    col_left, col_right = st.columns([4, 1])

    with col_left:
        st.markdown("### HR Accounts")
        st.caption("View and manage HR accounts across departments.")

    with col_right:
        add_hr = st.button(
            "＋ Add HR",
            use_container_width=True,
            type="primary",
        )

    # ---------------------------------------------------------
    # ADD HR FORM
    # ---------------------------------------------------------
    if add_hr:
        st.session_state["show_add_hr"] = True

    if st.session_state.get("show_add_hr", False):

        st.markdown("---")

        st.markdown("### ➕ Add New HR")

        department_data, department_error = api_request(
            "GET",
            "/admin/departments"
        )

        if department_error:
            st.error(department_error)
            return

        departments = (
            department_data.get("departments", [])
            if isinstance(department_data, dict)
            else []
        )

        if not departments:
            st.warning("No departments are available.")
            return

        department_options = {
            f'{d["department_name"]}': d["department_id"]
            for d in departments
        }

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input(
                    "First Name",
                    placeholder="Enter first name",
                )

                email = st.text_input(
                    "Email",
                    placeholder="Enter email address",
                )

                phone = st.text_input(
                    "Phone",
                    placeholder="Enter phone number",
                )

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                )

                dob = st.date_input(
                    "Date of Birth"
                )

            with col2:
                last_name = st.text_input(
                    "Last Name",
                    placeholder="Enter last name",
                )

                designation = st.text_input(
                    "Designation",
                    value="HR Manager",
                )

                department_name = st.selectbox(
                    "Department",
                    list(department_options.keys()),
                )

                joining_date = st.date_input(
                    "Joining Date"
                )

                base_salary = st.number_input(
                    "Base Salary",
                    min_value=0.0,
                    step=1000.0,
                )

            education = st.text_input(
                "Education",
                placeholder="e.g. MBA, BBA, MHRM",
            )

            skills = st.text_area(
                "Skills",
                placeholder="e.g. Recruitment, Payroll, Employee Relations",
                height=100,
            )

            st.markdown("")

            form_col1, form_col2 = st.columns(2)

            with form_col1:
                create_hr = st.button(
                    "✓ Create HR Account",
                    use_container_width=True,
                    type="primary",
                )

            with form_col2:
                cancel_hr = st.button(
                    "Cancel",
                    use_container_width=True,
                )

            if cancel_hr:
                st.session_state["show_add_hr"] = False
                st.rerun()

            if create_hr:

                if not first_name.strip():
                    st.error("First name is required.")
                    return

                if not last_name.strip():
                    st.error("Last name is required.")
                    return

                if not email.strip():
                    st.error("Email is required.")
                    return

                selected_department_id = department_options[
                    department_name
                ]

                payload = {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "email": email.strip(),
                    "phone": phone.strip(),
                    "gender": gender,
                    "dob": str(dob),
                    "joining_date": str(joining_date),
                    "department_id": selected_department_id,
                    "designation": designation.strip(),
                    "education": education.strip(),
                    "skills": skills.strip(),
                    "base_salary": base_salary,
                }

                result, create_error = api_request(
                    "POST",
                    "/admin/hr/add",
                    json=payload,
                )

                if create_error:
                    st.error(create_error)
                    return

                st.success(
                    result.get(
                        "message",
                        "HR account created successfully."
                    )
                )

                if isinstance(result, dict):
                    st.info(
                        f"HR ID: {result.get('hr_id', 'N/A')}  |  "
                        f"Username: {result.get('username', 'N/A')}  |  "
                        f"Temporary Password: "
                        f"{result.get('temporary_password', 'N/A')}"
                    )

                st.session_state["show_add_hr"] = False
                st.rerun()

    # ---------------------------------------------------------
    # HR TABLE
    # ---------------------------------------------------------
    st.markdown("---")

    if not hr_list:
        st.info("No HR accounts found.")
        return

    for hr in hr_list:

        hr_id = hr.get("hr_id", "N/A")
        full_name = (
            f'{hr.get("first_name", "")} '
            f'{hr.get("last_name", "")}'
        ).strip()

        department = hr.get(
            "department_name",
            "Unassigned"
        )

        status = hr.get(
            "status",
            "Unknown"
        )

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [2, 3, 2.5, 1.5]
            )

            with col1:
                st.markdown(f"**{hr_id}**")
                st.caption("HR ID")

            with col2:
                st.markdown(f"**{full_name}**")
                st.caption(hr.get("email", "No email"))

            with col3:
                st.markdown(f"**{department}**")
                st.caption(
                    hr.get(
                        "designation",
                        "HR"
                    )
                )

            with col4:
                if str(status).lower() == "active":
                    st.success("Active")
                else:
                    st.warning(status)

            st.divider()

            info1, info2, info3 = st.columns(3)

            with info1:
                st.caption("Phone")
                st.write(hr.get("phone") or "—")

            with info2:
                st.caption("Username")
                st.write(hr.get("username") or "—")

            with info3:
                st.caption("Salary")
                salary = hr.get("base_salary")

                if salary is not None:
                    st.write(f"₹{float(salary):,.0f}")
                else:
                    st.write("—")

            delete_col, _ = st.columns([1, 5])

            with delete_col:
                if st.button(
                    "🗑 Delete",
                    key=f"delete_hr_{hr_id}",
                    use_container_width=True,
                ):
                    st.session_state[
                        "delete_hr_id"
                    ] = hr_id

            if st.session_state.get("delete_hr_id") == hr_id:

                st.warning(
                    f"Are you sure you want to delete "
                    f"**{full_name} ({hr_id})**?"
                )

                yes_col, no_col = st.columns(2)

                with yes_col:
                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_delete_{hr_id}",
                        use_container_width=True,
                        type="primary",
                    ):
                        result, delete_error = api_request(
                            "DELETE",
                            f"/admin/hr/delete/{hr_id}",
                        )

                        if delete_error:
                            st.error(delete_error)
                        else:
                            st.success(
                                result.get(
                                    "message",
                                    "HR deleted successfully."
                                )
                            )

                            st.session_state[
                                "delete_hr_id"
                            ] = None

                            st.rerun()

                with no_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_{hr_id}",
                        use_container_width=True,
                    ):
                        st.session_state[
                            "delete_hr_id"
                        ] = None
                        st.rerun()