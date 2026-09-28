import streamlit as st
from src.patient_data import load_patients


def show_history():

    st.title("Assessment History")
    st.write("View and manage previous CVM assessments.")

    patients = load_patients()

    assessment_history = [
        [
            patient["patient_id"],
            patient["name"],
            patient["last_visit"],
            patient["visit_reason"],
            patient["stage"],
            {
                "CS1": "Pre-growth",
                "CS2": "Acceleration",
                "CS3": "Peak growth",
                "CS4": "Peak growth",
                "CS5": "Maturation",
                "CS6": "Post-growth"
            }.get(patient["stage"], "")
        ]
        for _, patient in patients.iterrows()
    ]

    # --------------------------------------------------
    # View Previous Assessment
    # --------------------------------------------------

    @st.dialog("Previous Assessment")
    def show_previous_assessment(patient):

        previous_stage = patient["previous_cvm_stage"]

        stage_data = {
            "CS1": {
                "growth_phase": "Pre-growth",
                "concavity": "None / None / None",
                "shape": "Trapezoid / Trapezoid / Trapezoid",
                "confidence": "90.5%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that the patient is in the pre-growth stage "
                    "of mandibular development."
                )
            },

            "CS2": {
                "growth_phase": "Acceleration of Growth Begins",
                "concavity": "Moderate / Moderate / Moderate",
                "shape": "Rectangular Horizontal / Trapezoidal / Trapezoidal",
                "confidence": "91.8%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that mandibular growth acceleration has begun."
                )
            },

            "CS3": {
                "growth_phase": "Peak Growth Approaching",
                "concavity": "Moderate / Deep / Deep",
                "shape": "Trapezoidal / Rectangular Horizontal / Square",
                "confidence": "92.0%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that the patient is approaching the peak "
                    "mandibular growth period."
                )
            },

            "CS4": {
                "growth_phase": "Peak Growth Passed Recently",
                "concavity": "Deep / Moderate / Moderate",
                "shape": "Trapezoid / Square / Rectangular Horizontal",
                "confidence": "92.4%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that the peak mandibular growth period has "
                    "recently passed."
                )
            },

            "CS5": {
                "growth_phase": "Growth Deceleration",
                "concavity": "Deep / Deep / Deep",
                "shape": "Square / Rectangular Vertical / Rectangular Vertical",
                "confidence": "93.2%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that mandibular growth is decelerating and "
                    "approaching completion."
                )
            },

            "CS6": {
                "growth_phase": "Growth Completed",
                "concavity": "Deep / Deep / Deep",
                "shape": "Rectangular Vertical / Rectangular Vertical / Rectangular Vertical",
                "confidence": "94.1%",
                "interpretation": (
                    "The morphological characteristics of C2, C3, and C4 "
                    "indicate that mandibular growth has essentially been "
                    "completed."
                )
            }
        }

        result = stage_data.get(previous_stage, {
            "growth_phase": "—",
            "concavity": "—",
            "shape": "—",
            "confidence": "—",
            "interpretation": "No previous assessment information available."
        })

        # --------------------------------------------------
        # Patient Information
        # --------------------------------------------------

        st.markdown("### Patient Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Patient ID:** {patient['patient_id']}")
            st.write(f"**Name:** {patient['name']}")
            st.write(f"**Date of Birth:** {patient['date_of_birth']}")
            st.write(f"**Age:** {patient['age']}")

        with col2:
            st.write(f"**Gender:** {patient['gender']}")
            st.write(f"**Last Visit:** {patient['last_visit']}")
            st.write(f"**Visit Reason:** {patient['visit_reason']}")
            st.write(f"**Referring Doctor:** {patient['referring_doctor']}")

        st.markdown("---")

        # --------------------------------------------------
        # Previous Assessment
        # --------------------------------------------------

        st.markdown("### Previous Assessment")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Previous CVM Stage:** {previous_stage}")

        with col2:
            st.write(f"**Growth Phase:** {result['growth_phase']}")

        st.markdown("---")

        # --------------------------------------------------
        # Automated Clinical Report Summary
        # --------------------------------------------------

        st.markdown("### Automated Clinical Report Summary")

        st.write(
            f"**Predicted CVM Stage:** {previous_stage}"
        )

        st.write(
            f"**Growth Phase:** {result['growth_phase']}"
        )

        st.write(
            f"**Concavity (C2/C3/C4):** {result['concavity']}"
        )

        st.write(
            f"**Shape (C2/C3/C4):** {result['shape']}"
        )

        st.write(
            f"**Confidence:** {result['confidence']}"
        )

        st.write(
            f"**Clinical Interpretation:** {result['interpretation']}"
        )

        st.markdown("---")

        # --------------------------------------------------
        # Clinical Information
        # --------------------------------------------------

        st.markdown("### Clinical Information")

        st.write(
            f"**Medical History:** "
            f"{patient['medical_history']}"
        )

        st.write(
            f"**Dental History:** "
            f"{patient['dental_history']}"
        )

        st.write(
            f"**Clinic:** "
            f"{patient['clinic']}"
        )

    # --------------------------------------------------
    # Assessment History Card
    # --------------------------------------------------

    with st.container(key="history-card"):

        st.subheader("Assessment History")

        # Search and filter
        col1, col2 = st.columns([3, 1])

        with col1:
            search = st.text_input(
                "Search",
                placeholder="🔍 Search by patient name or ID...",
                label_visibility="collapsed"
            )

        with col2:
            stage_filter = st.selectbox(
                "CVM Stage",
                [
                    "All CVM Stages",
                    "CS1",
                    "CS2",
                    "CS3",
                    "CS4",
                    "CS5",
                    "CS6"
                ],
                label_visibility="collapsed"
            )

        # Header
        col1, col2, col3, col4, col5, col6 = st.columns(
            [2.5, 1.2, 1.2, 1.2, 1.5, 2.0]
        )

        col1.write("**PATIENT ID**  \n**PATIENT NAME**")
        col2.write("**DATE**")
        col3.write("**VISIT REASON**")
        col4.write("**CVM STAGE**")
        col5.write("**GROWTH PHASE**")

        with col6:
            st.markdown(
                "<div style='text-align:center;'><b>ACTIONS</b></div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<hr style='margin: 5px 0; border: none; "
            "border-top: 1px solid #D1D5DB;'>",
            unsafe_allow_html=True
        )

        # Filter data
        filtered_history = assessment_history

        if search:
            filtered_history = [
                assessment for assessment in filtered_history
                if search.lower() in assessment[0].lower()
                or search.lower() in assessment[1].lower()
            ]

        if stage_filter != "All CVM Stages":
            filtered_history = [
                assessment for assessment in filtered_history
                if assessment[4] == stage_filter
            ]

        # Patient rows
        for i, assessment in enumerate(filtered_history):

            col1, col2, col3, col4, col5, col6 = st.columns(
                [2.5, 1.2, 1.2, 1.2, 1.5, 2.0]
            )

            col1.write(
                f"**{assessment[0]}**  \n{assessment[1]}"
            )

            col2.write(assessment[2])
            col3.write(assessment[3])
            col4.write(assessment[4])
            col5.write(assessment[5])

            with col6:

                btn1, btn2 = st.columns(2)

                with btn1:
                    with st.container(
                        key=f"history-view-{assessment[0]}"
                    ):
                        if st.button(
                            "View",
                            key=f"history_view_{assessment[0]}",
                            use_container_width=True
                        ):
                            patient = patients[
                                patients["patient_id"] == assessment[0]
                            ].iloc[0]

                            show_previous_assessment(patient)

                # with btn2:
                #     with st.container(
                #         key=f"history-delete-{assessment[0]}"
                #     ):
                #         st.button(
                #             "Delete",
                #             key=f"history_delete_{assessment[0]}",
                #             use_container_width=True
                #         )

            if i < len(filtered_history) - 1:
                st.markdown(
                    "<hr style='margin: 5px 0; border: none; "
                    "border-top: 1px solid #E5E7EB;'>",
                    unsafe_allow_html=True
                )