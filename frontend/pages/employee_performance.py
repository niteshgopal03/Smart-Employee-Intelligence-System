import streamlit as st

from api.client import api_request
from components.cards import section_header


def show_employee_performance():
    st.markdown(
        """
        <style>
        .performance-hero {
            padding: 30px;
            border-radius: 22px;
            background: linear-gradient(
                135deg,
                #1e1b4b 0%,
                #4338ca 55%,
                #6366f1 100%
            );
            color: white;
            margin-bottom: 25px;
            box-shadow: 0 14px 38px rgba(67, 56, 202, 0.22);
        }

        .performance-hero h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 750;
        }

        .performance-hero p {
            margin: 8px 0 0;
            color: #e0e7ff;
            font-size: 15px;
        }

        .score-card {
            padding: 24px;
            border-radius: 18px;
            border: 1px solid #e0e7ff;
            background: linear-gradient(
                145deg,
                #ffffff,
                #f5f7ff
            );
            text-align: center;
        }

        .score-label {
            color: #64748b;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .score-value {
            color: #4338ca;
            font-size: 44px;
            font-weight: 800;
            margin-top: 5px;
        }

        .score-subtitle {
            color: #64748b;
            font-size: 13px;
        }

        .info-card {
            padding: 20px;
            border-radius: 16px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="performance-hero">
            <h1>⭐ My Performance</h1>
            <p>
                View your current manager rating and performance information.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    employee_id = st.session_state.get("employee_id")

    if not employee_id:
        st.error("Employee information is missing from the current session.")
        return

   
    # Get own performance
   

    performance, error = api_request(
        "GET",
        f"/performance/{employee_id}",
    )

    if error:
        st.error(error)
        return

    performance = performance or {}

    manager_rating = performance.get("manager_rating")

    if manager_rating is None:
        st.info(
            "Your performance has not been rated yet."
        )
        return

    try:
        manager_rating = float(manager_rating)
    except (TypeError, ValueError):
        st.error("The performance rating returned by the backend is invalid.")
        return

   
    # Score
   

    score_col, info_col = st.columns([1, 2])

    with score_col:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">
                    Manager Rating
                </div>
                <div class="score-value">
                    {manager_rating:.1f}
                </div>
                <div class="score-subtitle">
                    out of 5.0
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info_col:
        st.markdown(
            """
            <div class="info-card">
                <h3>📌 Performance rating</h3>
                <p>
                    This rating is provided through the HR performance
                    management workflow. It may also be used as an input
                    for the employee intelligence features.
                </p>
                <p>
                    If you have questions about your rating, please contact
                    your HR representative.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

   
    # Rating scale
   

    section_header(
        "Rating scale",
        "The manager rating is measured on a 0–5 scale.",
    )

    rating_rows = [
        {"Rating": "0.0 – 1.0", "Level": "Very low"},
        {"Rating": "1.1 – 2.0", "Level": "Needs improvement"},
        {"Rating": "2.1 – 3.0", "Level": "Developing"},
        {"Rating": "3.1 – 4.0", "Level": "Good"},
        {"Rating": "4.1 – 5.0", "Level": "Excellent"},
    ]

    st.table(rating_rows)