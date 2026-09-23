import streamlit as st

from api.client import api_request


def show_admin_departments():

    st.title("🏢 Department Management")
    st.caption(" Create, update and manage organizational departments.")
    
    # LOAD DEPARTMENTS
   

    data, error = api_request(
        "GET",
        "/admin/departments"
    )

    if error:
        st.error(error)
        return

    departments = (
        data.get("departments", [])
        if isinstance(data, dict)
        else []
    )

    
    # METRICS
    

    total_departments = len(departments)

    total_employees = sum(
        int(department.get("total_employees", 0) or 0)
        for department in departments
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Departments",
            total_departments
        )

    with col2:
        st.metric(
            "Assigned Employees",
            total_employees
        )

    st.markdown("<br>", unsafe_allow_html=True)

    
    # ADD DEPARTMENT
    

    top_left, top_right = st.columns([4, 1])

    with top_left:
        st.markdown("### Departments")
        st.caption(
            "Manage departments used throughout the employee system."
        )

    with top_right:
        if st.button(
            "＋ Add Department",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["show_add_department"] = True

    
    # ADD DEPARTMENT FORM
    

    if st.session_state.get(
        "show_add_department",
        False
    ):

        st.markdown("---")
        st.markdown("### ➕ Add Department")

        with st.container(border=True):

            department_name = st.text_input(
                "Department Name",
                placeholder="e.g. Operations",
            )

            description = st.text_area(
                "Description",
                placeholder="Brief description of the department",
                height=100,
            )

            col1, col2 = st.columns(2)

            with col1:
                create_department = st.button(
                    "✓ Create Department",
                    use_container_width=True,
                    type="primary",
                )

            with col2:
                cancel_department = st.button(
                    "Cancel",
                    use_container_width=True,
                )

            if cancel_department:
                st.session_state[
                    "show_add_department"
                ] = False
                st.rerun()

            if create_department:

                if not department_name.strip():
                    st.error(
                        "Department name is required."
                    )
                    return

                payload = {
                    "department_name":
                        department_name.strip(),
                    "description":
                        description.strip() or None,
                }

                result, create_error = api_request(
                    "POST",
                    "/admin/departments",
                    json=payload,
                )

                if create_error:
                    st.error(create_error)
                    return

                message = (
                    result.get(
                        "message",
                        "Department created successfully."
                    )
                    if isinstance(result, dict)
                    else "Department created successfully."
                )

                st.success(message)

                st.session_state[
                    "show_add_department"
                ] = False

                st.rerun()

    

    st.markdown("---")

    if not departments:
        st.info(
            "No departments found."
        )
        return

    for department in departments:

        department_id = department.get(
            "department_id"
        )

        department_name = department.get(
            "department_name",
            "Unnamed Department"
        )

        description = department.get(
            "description"
        ) or "No description provided."

        employee_count = int(
            department.get(
                "total_employees",
                0
            ) or 0
        )

        active_count = int(
            department.get(
                "active_employees",
                0
            ) or 0
        )

        resigned_count = int(
            department.get(
                "resigned_employees",
                0
            ) or 0
        )

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [3, 3, 1.5, 1.5]
            )

            with col1:
                st.markdown(
                    f"### 🏢 {department_name}"
                )
                st.caption(
                    f"Department ID: {department_id}"
                )

            with col2:
                st.write(description)

            with col3:
                st.metric(
                    "Employees",
                    employee_count
                )

            with col4:
                st.metric(
                    "Active",
                    active_count
                )

            st.divider()

            info1, info2, info3 = st.columns(3)

            with info1:
                st.caption("Total Employees")
                st.write(employee_count)

            with info2:
                st.caption("Active Employees")
                st.write(active_count)

            with info3:
                st.caption("Resigned Employees")
                st.write(resigned_count)

            st.markdown("")

            edit_col, delete_col, empty = st.columns(
                [1, 1, 4]
            )

            with edit_col:
                if st.button(
                    "✏️ Edit",
                    key=f"edit_department_{department_id}",
                    use_container_width=True,
                ):
                    st.session_state[
                        "edit_department_id"
                    ] = department_id

            with delete_col:
                if st.button(
                    "🗑 Delete",
                    key=f"delete_department_{department_id}",
                    use_container_width=True,
                ):
                    st.session_state[
                        "delete_department_id"
                    ] = department_id

            

            if st.session_state.get(
                "edit_department_id"
            ) == department_id:

                st.markdown("---")
                st.markdown("#### ✏️ Edit Department")

                edit_name = st.text_input(
                    "Department Name",
                    value=department_name,
                    key=f"edit_name_{department_id}",
                )

                edit_description = st.text_area(
                    "Description",
                    value=description
                    if description != "No description provided."
                    else "",
                    key=f"edit_description_{department_id}",
                    height=100,
                )

                save_col, cancel_col = st.columns(2)

                with save_col:
                    if st.button(
                        "✓ Save Changes",
                        key=f"save_department_{department_id}",
                        use_container_width=True,
                        type="primary",
                    ):

                        if not edit_name.strip():
                            st.error(
                                "Department name is required."
                            )
                            return

                        payload = {
                            "department_name":
                                edit_name.strip(),
                            "description":
                                edit_description.strip()
                                or None,
                        }

                        result, update_error = api_request(
                            "PUT",
                            f"/admin/departments/{department_id}",
                            json=payload,
                        )

                        if update_error:
                            st.error(update_error)
                        else:
                            st.success(
                                result.get(
                                    "message",
                                    "Department updated successfully."
                                )
                            )

                            st.session_state[
                                "edit_department_id"
                            ] = None

                            st.rerun()

                with cancel_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_edit_{department_id}",
                        use_container_width=True,
                    ):
                        st.session_state[
                            "edit_department_id"
                        ] = None
                        st.rerun()

            

            if st.session_state.get(
                "delete_department_id"
            ) == department_id:

                st.markdown("---")

                if employee_count > 0:

                    st.warning(
                        f"**{department_name}** cannot be deleted "
                        f"because {employee_count} employee(s) "
                        f"are assigned to this department."
                    )

                    if st.button(
                        "Close",
                        key=f"close_delete_{department_id}",
                    ):
                        st.session_state[
                            "delete_department_id"
                        ] = None
                        st.rerun()

                else:

                    st.warning(
                        f"Are you sure you want to delete "
                        f"**{department_name}**?"
                    )

                    yes_col, no_col = st.columns(2)

                    with yes_col:
                        if st.button(
                            "Yes, Delete",
                            key=f"confirm_delete_{department_id}",
                            use_container_width=True,
                            type="primary",
                        ):

                            result, delete_error = api_request(
                                "DELETE",
                                f"/admin/departments/{department_id}",
                            )

                            if delete_error:
                                st.error(delete_error)
                            else:
                                st.success(
                                    result.get(
                                        "message",
                                        "Department deleted successfully."
                                    )
                                )

                                st.session_state[
                                    "delete_department_id"
                                ] = None

                                st.rerun()

                    with no_col:
                        if st.button(
                            "Cancel",
                            key=f"cancel_delete_{department_id}",
                            use_container_width=True,
                        ):
                            st.session_state[
                                "delete_department_id"
                            ] = None
                            st.rerun()