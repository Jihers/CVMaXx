import streamlit as st


@st.dialog("Upload X-Ray Image", width="small")
def show_ai_analysis(patient):

    # Popup styling
    st.markdown("""
        <style>
        /* Patient card */
        .patient-card {
            background: #EFFBFD;
            border: 1px solid #BFE8EF;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 18px;
        }

        .patient-name {
            font-size: 16px;
            font-weight: 600;
            color: #263238;
        }

        .patient-info {
            font-size: 13px;
            color: #78909C;
            margin-top: 2px;
        }

        /* Upload area */
        [data-testid="stFileUploader"] {
            border: 2px dashed #CBD5DC;
            border-radius: 16px;
            padding: 20px 12px;
            background: #FAFCFD;
        }

        [data-testid="stFileUploaderDropzone"] {
            border: none;
            background: transparent;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 12px;
            height: 46px;
            font-size: 15px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Patient information
    st.markdown(
        f"""
        <div class="patient-card">
            <div class="patient-name">🧑🏻‍⚕️ &nbsp; {patient[1]}</div>
            <div class="patient-info">
                {patient[0]} &nbsp;·&nbsp; {patient[2]}y &nbsp; {patient[3]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # X-ray upload
    uploaded_file = st.file_uploader(
        "Upload Lateral Cephalogram",
        type=["png", "jpg", "jpeg", "dcm"],
        help="PNG, JPG, or DICOM"
    )

    # Preview uploaded X-ray
    if uploaded_file is not None:

        st.markdown(
            """
            <div style="
                font-size: 14px;
                font-weight: 600;
                color: #37474F;
                margin-top: 8px;
                margin-bottom: 8px;
            ">
                X-Ray Preview
            </div>
            """,
            unsafe_allow_html=True
        )

        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(
                uploaded_file,
                width="stretch"
            )

        else:
            st.info("DICOM file uploaded successfully.")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        cancel = st.button(
            "Cancel",
            use_container_width=True
        )

    with col2:
        start = st.button(
            "Start AI Analysis",
            type="primary",
            use_container_width=True
        )

    if cancel:
        st.rerun()

    if start:
        if uploaded_file is None:
            st.warning("Please upload an X-ray image first.")
        else:
            st.session_state["selected_patient"] = patient
            st.session_state["uploaded_xray"] = uploaded_file
            st.session_state["show_results"] = True
            st.session_state["page"] = "CVM Assessment"

            st.rerun()