import streamlit as st
import plotly.express as px


def show_dashboard():
    
    st.title("Dashboard")

    st.markdown("""
    **Welcome to CVMaXx**  
    An AI-assisted cervical vertebral maturation assessment system.
    """)

    st.divider()

    # ----------------------------------------------
    # Statistic cards
    # ----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total X-rays",
            value="128",
            delta="12 this month"
        )

    with col2:
        st.metric(
            label="Total Patients",
            value="86",
            delta="8 this month"
        )

    with col3:
        st.metric(
            label="Model Accuracy",
            value="94.2%",
            delta="2.1%"
        )

    with col4:
        st.metric(
            label="Assessments",
            value="128",
            delta="15 this month"
        )

    st.divider()

    # ----------------------------------------------
    # Recent predictions
    # ----------------------------------------------

    st.subheader("Recent Predictions")

    recent_predictions = {
        "Patient": [
            "Patient 001",
            "Patient 002",
            "Patient 003",
            "Patient 004",
            "Patient 005"
        ],
        "CVM Stage": [
            "CS2",
            "CS3",
            "CS4",
            "CS2",
            "CS5"
        ],
        "Growth Phase": [
            "Pre-Growth",
            "Peak Growth",
            "Post-Growth",
            "Pre-Growth",
            "Post-Growth"
        ],
        "Date": [
            "14 Sep 2026",
            "13 Sep 2026",
            "13 Sep 2026",
            "12 Sep 2026",
            "11 Sep 2026"
        ]
    }

    st.dataframe(
        recent_predictions,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ----------------------------------------------
    # Charts
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("CVM Stage Distribution")

        cvm_distribution = {
            "CS1": 18,
            "CS2": 27,
            "CS3": 31,
            "CS4": 24,
            "CS5": 19,
            "CS6": 9
        }

        st.bar_chart(cvm_distribution)

    with col2:

        st.subheader("Growth Phase Distribution")

        growth_phase = {
            "Pre-growth": 45,
            "Peak Growth": 55,
            "Post-growth": 28
        }

        fig = px.pie(
            names=list(growth_phase.keys()),
            values=list(growth_phase.values()),
            hole=0.4
        )

        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ----------------------------------------------
    # Growth Phase Summary
    # ----------------------------------------------

    st.subheader("Growth Phase Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div style="
                background-color: #FFFFFF;
                border: 1px solid #DDE4F2;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.10);
                height: 220px;
                box-sizing: border-box;
            ">
                <h4 style="color: #1F2937; margin-bottom: 8px;">
                    Pre-growth Phase (CS1–CS2)
                </h4>
                <h2 style="color: #1F2937; margin-bottom: 10px;">
                    45 patients
                </h2>
                <p style="color: #667085; font-size: 14px;">
                    Early skeletal maturation stage.
                    No significant growth spurt expected.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div style="
                background-color: #FFFFFF;
                border: 1px solid #DDE4F2;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.10);
                height: 220px;
                box-sizing: border-box;
            ">
                <h4 style="color: #1F2937; margin-bottom: 8px;">
                    Peak Growth Phase (CS3–CS4)
                </h4>
                <h2 style="color: #1F2937; margin-bottom: 10px;">
                    55 patients
                </h2>
                <p style="color: #667085; font-size: 14px;">
                    Optimal timing for growth modification
                    treatment.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div style="
                background-color: #FFFFFF;
                border: 1px solid #DDE4F2;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.10);
                height: 220px;
                box-sizing: border-box;
            ">
                <h4 style="color: #1F2937; margin-bottom: 8px;">
                    Post-growth Phase (CS5–CS6)
                </h4>
                <h2 style="color: #1F2937; margin-bottom: 10px;">
                    28 patients
                </h2>
                <p style="color: #667085; font-size: 14px;">
                    Growth spurt completed.
                    Consider alternative treatment options.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )