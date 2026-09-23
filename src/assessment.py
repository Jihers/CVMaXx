import streamlit as st

from src.ai_analysis import show_ai_analysis

def show_assessment():
    st.title("CVM Assessment")
    st.write("Select a patient to view details or perform an AI-assisted analysis.")

    patients = [
        ["P001", "John Smith", 14, "Male", "2026-05-01"],
        ["P002", "Emma Johnson", 13, "Female", "2026-04-28"],
        ["P003", "Michael Brown", 15, "Male", "2026-05-03"],
        ["P004", "Sophia Davis", 12, "Female", "2026-04-25"],
        ["P005", "William Wilson", 16, "Male", "2026-05-05"],
    ]

    # --------------------------------------------------
    # Patient List Card
    # --------------------------------------------------

    with st.container(key="patient-card"):

        st.subheader("Patient List")

        search = st.text_input(
            "Search",
            placeholder="🔍 Search by patient name or ID...",
            label_visibility="collapsed"
        )

        # Header
        col1, col2, col3, col4, col5 = st.columns(
            [2.5, 0.7, 1, 1.3, 2.4]
        )

        col1.write("**PATIENT**")
        col2.write("**AGE**")
        col3.write("**GENDER**")
        col4.write("**LAST VISIT**")

        with col5:
            st.markdown(
                "<div style='text-align:center;'><b>ACTIONS</b></div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<hr style='margin: 5px 0; border: none; border-top: 1px solid #D1D5DB;'>",
            unsafe_allow_html=True
        )

        # Patient rows
        for i, patient in enumerate(patients):

            col1, col2, col3, col4, col5 = st.columns(
                [2.5, 0.7, 1, 1.3, 2.4]
            )

            col1.write(f"**{patient[1]}**  \n{patient[0]}")
            col2.write(patient[2])
            col3.write(patient[3])
            col4.write(patient[4])

            with col5:
                btn1, btn2 = st.columns(2)

                with btn1:
                    with st.container(key=f"view-details-{patient[0]}"):
                        st.button(
                            "View Details",
                            key=f"view_{patient[0]}",
                            use_container_width=True
                        )

                with btn2:
                    with st.container(key=f"ai-analysis-{patient[0]}"):
                        if st.button(
                            "AI Analysis",
                            key=f"ai_{patient[0]}",
                            use_container_width=True
                        ):
                            show_ai_analysis(patient)

            if i < len(patients) - 1:
                st.markdown(
                    "<hr style='margin: 5px 0; border: none; border-top: 1px solid #E5E7EB;'>",
                    unsafe_allow_html=True
                )