import streamlit as st

from api.client import api_request
from api.ai_api import (
    predict_salary,
    predict_promotion,
    predict_attrition,
)


def show_hr_ai_prediction():

    

    st.title(" AI Employee Prediction")

    st.caption(
        "Use the employee's current workforce data to generate "
        "AI-assisted salary, promotion, and attrition predictions."
    )

    st.write("")

    

    employees_data, employees_error = api_request(
        "GET",
        "/employees/search",
        params={"search": ""},
    )

    if employees_error:
        st.error(
            f"Unable to load employees: {employees_error}"
        )
        return

    if isinstance(employees_data, dict):
        employees = employees_data.get(
            "employees",
            []
        )
    elif isinstance(employees_data, list):
        employees = employees_data
    else:
        employees = []

    if not employees:
        st.info(
            "No employees are available for AI prediction."
        )
        return

    
    # EMPLOYEE SELECTION
    

    employee_options = {}

    for employee in employees:

        employee_id = employee.get(
            "employee_id"
        )

        first_name = employee.get(
            "first_name",
            ""
        )

        last_name = employee.get(
            "last_name",
            ""
        )

        full_name = (
            f"{first_name} {last_name}"
        ).strip()

        if employee_id:
            employee_options[
                f"{full_name} — {employee_id}"
            ] = employee_id

    if not employee_options:
        st.warning(
            "No valid employee records were found."
        )
        return

    selected_label = st.selectbox(
        "Select Employee",
        list(employee_options.keys()),
    )

    selected_employee_id = employee_options[
        selected_label
    ]

    st.write("")

   

    st.subheader("Prediction Center")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("### 💰")

            st.markdown(
                "**Salary Prediction**"
            )

            st.caption(
                "Estimate the employee's predicted salary "
                "from the current workforce profile."
            )

            salary_button = st.button(
                "Run Salary Prediction",
                use_container_width=True,
                key="salary_prediction",
            )

    with col2:

        with st.container(border=True):

            st.markdown("### 📈")

            st.markdown(
                "**Promotion Prediction**"
            )

            st.caption(
                "Estimate whether the employee is likely "
                "to be promotion-ready."
            )

            promotion_button = st.button(
                "Run Promotion Prediction",
                use_container_width=True,
                key="promotion_prediction",
            )

    with col3:

        with st.container(border=True):

            st.markdown("### ⚠️")

            st.markdown(
                "**Attrition Prediction**"
            )

            st.caption(
                "Estimate the employee's current "
                "attrition risk level."
            )

            attrition_button = st.button(
                "Run Attrition Prediction",
                use_container_width=True,
                key="attrition_prediction",
            )

  

    if salary_button:

        with st.spinner(
            "Generating salary prediction..."
        ):

            result, error = predict_salary(
                selected_employee_id
            )

        if error:

            st.error(error)

        else:

            predicted_salary = result.get(
                "predicted_salary"
            )

            st.write("")

            with st.container(border=True):

                st.markdown(
                    "### 💰 Predicted Salary"
                )

                if predicted_salary is not None:

                    st.metric(
                        "Estimated Annual Salary",
                        f"₹{predicted_salary:,.2f}",
                    )

                else:

                    st.warning(
                        "Salary prediction was returned "
                        "without a predicted salary."
                    )

    

    if promotion_button:

        with st.spinner(
            "Generating promotion prediction..."
        ):

            result, error = predict_promotion(
                selected_employee_id
            )

        if error:

            st.error(error)

        else:

            prediction = result.get(
                "promotion_prediction",
                "Unknown"
            )

            confidence = result.get(
                "confidence",
                0
            )

            reasons = result.get(
                "reasons",
                []
            )

            st.write("")

            with st.container(border=True):

                st.markdown(
                    "### 📈 Promotion Prediction"
                )

                metric_col1, metric_col2 = st.columns(2)

                with metric_col1:

                    st.metric(
                        "Prediction",
                        prediction,
                    )

                with metric_col2:

                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%",
                    )

                st.markdown(
                    "**Prediction Factors**"
                )

                for reason in reasons:

                    st.markdown(
                        f"• {reason}"
                    )

    

    if attrition_button:

        with st.spinner(
            "Generating attrition prediction..."
        ):

            result, error = predict_attrition(
                selected_employee_id
            )

        if error:

            st.error(error)

        else:

            risk = result.get(
                "attrition_risk",
                "Unknown"
            )

            probability = result.get(
                "high_risk_probability",
                0
            )

            confidence = result.get(
                "confidence",
                0
            )

            reasons = result.get(
                "reasons",
                []
            )

            st.write("")

            with st.container(border=True):

                st.markdown(
                    "### ⚠️ Attrition Risk Prediction"
                )

                metric_col1, metric_col2, metric_col3 = (
                    st.columns(3)
                )

                with metric_col1:

                    st.metric(
                        "Risk Level",
                        risk,
                    )

                with metric_col2:

                    st.metric(
                        "High-Risk Probability",
                        f"{probability:.2f}%",
                    )

                with metric_col3:

                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%",
                    )

                st.markdown(
                    "**Risk Factors**"
                )

                for reason in reasons:

                    st.markdown(
                        f"• {reason}"
                    )

   

    st.write("")

    with st.expander(
        "ℹ️ About AI Predictions"
    ):

        st.write(
            "Predictions are generated using the employee's "
            "current information and the trained machine "
            "learning models configured in the backend."
        )

        st.write(
            "The prediction results are generated on demand "
            "and are not stored as separate AI records."
        )