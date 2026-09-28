import streamlit as st
from src.patient_data import load_patients
from src.ai_analysis import show_ai_analysis

def show_assessment():
    st.title("CVM Assessment")
    st.write("Select a patient to view details or perform an AI-assisted analysis.")

    patients = load_patients()

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

        # Filter patients
        if search:
            search = search.lower()

            patients = patients[
                patients["name"].str.lower().str.contains(search, na=False)
                | patients["patient_id"].str.lower().str.contains(search, na=False)
            ]

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
        for i, patient in patients.iterrows():

            col1, col2, col3, col4, col5 = st.columns(
                [2.5, 0.7, 1, 1.3, 2.4]
            )

            col1.write(
                f"**{patient['name']}**  \n{patient['patient_id']}"
            )
            col2.write(patient['age'])
            col3.write(patient['gender'])
            col4.write(patient['last_visit'])

            with col5:
                btn1, btn2 = st.columns(2)

                with btn1:
                    with st.container(
                        key=f"view-details-{patient['patient_id']}"
                    ):
                        if st.button(
                            "View Details",
                            key=f"view_{patient['patient_id']}",
                            use_container_width=True
                        ):
                            show_patient_details(patient)

                with btn2:
                    with st.container(
                        key=f"ai-analysis-{patient['patient_id']}"
                    ):
                        if st.button(
                            "AI Analysis",
                            key=f"ai_{patient['patient_id']}",
                            use_container_width=True
                        ):
                            show_ai_analysis(patient)

            if i < len(patients) - 1:
                st.markdown(
                    "<hr style='margin: 5px 0; border: none; border-top: 1px solid #E5E7EB;'>",
                    unsafe_allow_html=True
                )


@st.dialog("Patient Details")
def show_patient_details(patient):

    # --------------------------------------------------
    # Patient Header
    # --------------------------------------------------

    st.markdown(
        f"""
        <div style="
            background-color: #F8FAFC;
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <div style="
                font-size: 22px;
                font-weight: 700;
                color: #173A72;
            ">
                {patient['name']}
            </div>
            <div style="
                font-size: 14px;
                color: #64748B;
                margin-top: 4px;
            ">
                Patient ID: {patient['patient_id']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Personal Information
    # --------------------------------------------------

    st.markdown(
        "<div style='font-size:17px; font-weight:600; "
        "color:#173A72; margin-bottom:12px;'>"
        "Personal Information</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**IC Number**  \n{patient['ic_number']}")
        st.markdown(f"**Date of Birth**  \n{patient['date_of_birth']}")
        st.markdown(f"**Age**  \n{patient['age']} years old")

    with col2:
        st.markdown(f"**Gender**  \n{patient['gender']}")
        st.markdown(f"**Phone Number**  \n{patient['phone']}")

    st.markdown(
        f"**Address**  \n{patient['address']}"
    )

    st.markdown("---")

    # --------------------------------------------------
    # Clinical Visit Information
    # --------------------------------------------------

    st.markdown(
        "<div style='font-size:17px; font-weight:600; "
        "color:#173A72; margin-bottom:12px;'>"
        "Clinical Visit Information</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Last Visit**  \n{patient['last_visit']}")
        st.markdown(f"**Visit Reason**  \n{patient['visit_reason']}")
        st.markdown(f"**Referring Doctor**  \n{patient['referring_doctor']}")

    with col2:
        st.markdown(f"**Clinic**  \n{patient['clinic']}")
        st.markdown(f"**Previous CVM Stage**  \n{patient['previous_cvm_stage']}")

    st.markdown("---")

    # --------------------------------------------------
    # Clinical History
    # --------------------------------------------------

    st.markdown(
        "<div style='font-size:17px; font-weight:600; "
        "color:#173A72; margin-bottom:12px;'>"
        "Clinical History</div>",
        unsafe_allow_html=True
    )

    st.markdown("**Medical History**")
    st.info(patient["medical_history"])

    st.markdown("**Dental History**")
    st.info(patient["dental_history"])