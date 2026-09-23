import streamlit as st
import streamlit.components.v1 as components

from src.dashboard import show_dashboard
from src.assessment import show_assessment
from src.history import show_history
from src.setting import show_setting
from src.result import show_results


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.markdown("""
<style>

    /* Keep header so sidebar toggle remains available */
    header {
        background: transparent !important;
    }

    /* Hide the three-dot menu */
    #MainMenu {
        display: none !important;
    }

    /* Hide footer */
    footer {
        display: none !important;
    }

    /* Reduce top spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="CVMaXx",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown("""
<style>

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DDE4F2;
    padding: 20px 22px;
    border-radius: 14px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10);
}

div[data-testid="stMetricLabel"] {
    color: #667085 !important;
    font-size: 14px;
    font-weight: 500;
}

div[data-testid="stMetricValue"] {
    color: #1F2937 !important;
    font-size: 28px;
    font-weight: 700;
}

div[data-testid="stMetricDelta"] {
    font-size: 13px;
}

/* Patient List Card */
.st-key-patient-card {
    background-color: #FFFFFF !important;
    border: 1px solid #DDE4F2 !important;
    padding: 20px 22px !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10);
}

.st-key-patient-card input {
    border: 1px solid #C9D2E3 !important;
    border-radius: 8px !important;
}

/* View Details - blue */
[class*="st-key-view-details-"] button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
}

/* AI Analysis - green */
[class*="st-key-ai-analysis-"] button {
    background-color: #16A34A !important;
    color: white !important;
    border: none !important;
}

/* Assessment History Card */
.st-key-history-card {
    background-color: #FFFFFF !important;
    border: 1px solid #DDE4F2 !important;
    padding: 20px 22px !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10);
}

/* History Search */
.st-key-history-card input {
    border: 1px solid #C9D2E3 !important;
    border-radius: 8px !important;
}

/* View button - blue */
[class*="st-key-history-view-"] button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
}

/* Delete button - red */
[class*="st-key-history-delete-"] button {
    background-color: #DC2626 !important;
    color: white !important;
    border: none !important;
}

 /* Settings Card */
.st-key-settings-card,
.st-key-about-card {
    background-color: #FFFFFF !important;
    border: 1px solid #DDE4F2 !important;
    padding: 20px 22px !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10);
}

.st-key-about-card {
    margin-top: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar Styling
# --------------------------------------------------

st.markdown("""
<style>

    /* All navigation buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        height: 48px !important;

        padding: 10px 14px !important;
        margin: 2px 0 !important;

        border: none !important;
        border-radius: 8px !important;

        background-color: transparent !important;
        color: #555 !important;

        font-size: 20px !important;
        font-weight: 500 !important;

        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* Hover */
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #F1EEFF !important;
        color: #4F2BED !important;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🦷 CVMaXx")
    st.caption("Cervical Vertebral Maturation")

    # Live date and time
    components.html(
        """
        <div style="
            font-family: Arial, sans-serif;
            color: #667085;
            font-size: 13px;
            line-height: 1.6;
            margin-top: 5px;
            margin-bottom: 5px;
        ">
            <div style="
                font-weight: 600;
                color: #1F2937;
            ">
                📅 <span id="date">Loading...</span>
            </div>

            <div>
                🕐 <span id="time">Loading...</span>
            </div>
        </div>

        <script>
            function updateClock() {
                const now = new Date();

                document.getElementById("date").textContent =
                    now.toLocaleDateString("en-MY", {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                        year: "numeric"
                    });

                document.getElementById("time").textContent =
                    now.toLocaleTimeString("en-MY", {
                        hour: "numeric",
                        minute: "2-digit",
                        second: "2-digit",
                        hour12: true
                    });
            }

            updateClock();
            setInterval(updateClock, 1000);
        </script>
        """,
        height=55
    )
    
    st.divider()

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    pages = {
        "Dashboard": "▦",
        "CVM Assessment": "☢",
        "Assessment History": "◷",
        "Settings": "⚙"
    }

    for name, icon in pages.items():
        if st.session_state.page == name:
            st.markdown(
                f"""
                <div style="
                    background:#4F2BED;
                    color:white;
                    padding:10px 14px;
                    border-radius:8px;
                    margin:2px 0;
                    font-size:20px;
                    font-weight:600;
                ">
                    {icon}&nbsp;&nbsp;{name}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:

            if st.button(
                f"{icon}   {name}",
                key=f"nav_{name}",
                use_container_width=True
            ):
                st.session_state.page = name
                st.rerun()

    st.divider()

    st.caption("CVMaXx v1.0")


page = st.session_state.page

if st.session_state.get("show_results", False): #Show sidebar if not in results view
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            max-width: 100% !important;
            padding: 1rem 2rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.get("show_results", False):

    # Full-page Results view
    show_results(
        st.session_state["selected_patient"],
        st.session_state["uploaded_xray"]
    )

else:

    if page == "Dashboard":
        show_dashboard()

    elif page == "CVM Assessment":
        show_assessment()

    elif page == "Assessment History":
        show_history()

    elif page == "Settings":
        show_setting()
    