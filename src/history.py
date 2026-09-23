import streamlit as st

def show_history():

    st.title("Assessment History")
    st.write("View and manage previous CVM assessments.")

    assessment_history = [
        ["P001", "John Smith", "6/25/2026", "3:10:45 PM", "CS4", "Peak growth"],
        ["P002", "Emma Johnson", "6/24/2026", "11:25:18 AM", "CS2", "Acceleration"],
        ["P003", "Michael Brown", "6/23/2026", "2:45:32 PM", "CS5", "Maturation"],
        ["P004", "Sophia Davis", "6/22/2026", "9:15:07 AM", "CS3", "Peak growth"],
        ["P005", "William Wilson", "6/20/2026", "4:30:21 PM", "CS1", "Pre-growth"],
    ]

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
        col3.write("**TIME**")
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
                        st.button(
                            "View",
                            key=f"history_view_{assessment[0]}",
                            use_container_width=True
                        )

                with btn2:
                    with st.container(
                        key=f"history-delete-{assessment[0]}"
                    ):
                        st.button(
                            "Delete",
                            key=f"history_delete_{assessment[0]}",
                            use_container_width=True
                        )

            if i < len(filtered_history) - 1:
                st.markdown(
                    "<hr style='margin: 5px 0; border: none; "
                    "border-top: 1px solid #E5E7EB;'>",
                    unsafe_allow_html=True
                )