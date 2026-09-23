import streamlit as st

def show_setting():
    st.title("Settings")
    st.write("Configure CVMaXx system preferences and assessment settings.")

    # --------------------------------------------------
    # General Settings
    # --------------------------------------------------

    with st.container(key="settings-card"):

        st.subheader("General Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Language",
                ["English"],
                help="Select the system language."
            )

        with col2:
            st.selectbox(
                "Date Format",
                ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
                index=0
            )

        st.divider()

        st.subheader("Assessment Settings")
        6

        st.checkbox(
            "Show assessment recommendations",
            value=True,
            help="Display treatment timing recommendations based on the predicted CVM stage."
        )

        st.checkbox(
            "Save assessment history automatically",
            value=True,
            help="Automatically save completed assessments to Assessment History."
        )

    with st.container(key="about-card"):

        st.subheader("About CVMaXx")

        st.markdown(
            """
            **Cervical Vertebrae Maturation Assessment System v1.0**

            Developed for orthodontic skeletal maturity evaluation
            """
        )