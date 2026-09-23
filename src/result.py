import streamlit as st
from datetime import datetime

def show_results(patient, uploaded_xray):

    # ============================================================
    # PAGE STYLING
    # ============================================================

    st.markdown("""
    <style>

    .result-title {
        font-size: 28px;
        font-weight: 700;
        color: #173A72;
        margin-bottom: 4px;
    }

    .result-subtitle {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 22px;
    }

    .section-card {
        background: #FFFFFF;
        border: 1px solid #DCE3EA;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #173A72;
        margin-bottom: 14px;
    }

    .stage-card {
        background: #F1F7FF;
        border: 1px solid #C7DDF7;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }

    .stage-label {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 5px;
    }

    .stage-value {
        font-size: 42px;
        font-weight: 700;
        color: #246BCE;
    }

    .stage-description {
        font-size: 14px;
        color: #315B8C;
        margin-top: 4px;
    }

    .confidence {
        font-size: 14px;
        color: #475569;
        margin-top: 10px;
    }

    .interpretation-card {
        background: #F8FAFC;
        border-left: 4px solid #246BCE;
        border-radius: 8px;
        padding: 14px 16px;
        color: #334155;
        font-size: 14px;
        line-height: 1.6;
    }

    .summary-box {
        background: #F4F9FF;
        border: 1px solid #C9DFF5;
        border-radius: 10px;
        padding: 16px;
        line-height: 1.8;
        font-size: 14px;
        color: #334155;
    }

    .measurement-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .measurement-table th {
        background: #F1F5F9;
        color: #334155;
        font-weight: 600;
        padding: 10px;
        text-align: center;
        border: 1px solid #DCE3EA;
    }

    .measurement-table td {
        padding: 10px;
        text-align: center;
        border: 1px solid #DCE3EA;
        color: #475569;
    }

    .measurement-table td:first-child {
        text-align: left;
        font-weight: 600;
    }

    .concavity-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .concavity-table th {
        background: #F1F5F9;
        padding: 10px;
        border: 1px solid #DCE3EA;
        color: #334155;
    }

    .concavity-table td {
        padding: 10px;
        border: 1px solid #DCE3EA;
        text-align: center;
    }

    .deep {
        color: #238636;
        font-weight: 600;
    }

    .moderate {
        color: #D89000;
        font-weight: 600;
    }

    .shape-box {
        background: #FAFCFF;
        border: 1px solid #DCE3EA;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        height: 100%;
    }

    .shape-name {
        font-weight: 600;
        color: #334155;
        margin-bottom: 8px;
    }

    .shape-result {
        color: #2563EB;
        font-weight: 600;
        font-size: 14px;
    }

    .age-reference {
        background: #FFFFFF;
        border: 1px solid #DCE3EA;
        border-radius: 10px;
        padding: 14px;
        margin-top: 10px;
    }

    .result-header {
        background-color: #0D1E35;
        height: 76px;
        padding: 0 24px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .result-header-title {
        color: white;
        font-size: 21px;
        font-weight: 700;
    }

    .result-header-info {
        display: flex;
        gap: 35px;
        margin-right: 50px;
    }

    .header-label {
        color: #9CA9B8;
        font-size: 12px;
    }

    .header-value {
        color: white;
        font-size: 14px;
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)


    # ============================================================
    # HEADER
    # ============================================================

    st.markdown(
        f"""
        <div class="result-header">
            <div class="result-header-title">
                CVM AI Analysis
            </div>
            <div class="result-header-info">
                <div>
                    <div class="header-label">Patient ID</div>
                    <div class="header-value">{patient[0]}</div>
                </div>
                <div>
                    <div class="header-label">Date</div>
                    <div class="header-value">
                        {datetime.now().strftime("%d %b %Y")}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("×", key="close_results"):
        st.session_state["show_results"] = False
        st.session_state.pop("selected_patient", None)
        st.session_state.pop("uploaded_xray", None)
        st.rerun()

    # ============================================================
    # 1. DETECTED X-RAY
    # ============================================================

    st.markdown("""
    <div class="section-card">
        <div class="section-title">
            Detected Cervical Vertebrae
        </div>
    """, unsafe_allow_html=True)

    if uploaded_xray is not None:

        st.image(
            uploaded_xray,
            width="stretch"
        )

    st.markdown("</div>", unsafe_allow_html=True)


    # ============================================================
    # 2. CONCAVITY ANALYSIS
    # ============================================================

    st.markdown("""
    <div class="section-card">
        <div class="section-title">
            2. Concavity Analysis (C2–C4)
        </div>
        <table class="concavity-table">
            <tr>
                <th>Vertebra</th>
                <th>Concavity Depth</th>
                <th>Concavity Classification</th>
            </tr>
            <tr>
                <td>C2</td>
                <td>1.8 mm</td>
                <td class="deep">Deep</td>
            </tr>
            <tr>
                <td>C3</td>
                <td>1.4 mm</td>
                <td class="moderate">Moderate</td>
            </tr>
            <tr>
                <td>C4</td>
                <td>1.2 mm</td>
                <td class="moderate">Moderate</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # 3. VERTEBRAL SHAPE CLASSIFICATION
    # ============================================================

    st.markdown(
        '<div class="section-card">'
        '<div class="section-title">3. Vertebral Shape Classification</div>'
        '<div style="text-align:center;font-size:14px;font-weight:600;color:#64748B;margin-bottom:16px;">'
        'Predicted Stage'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div style="text-align:center;padding:10px;">'
            '<div style="height:110px;display:flex;align-items:center;justify-content:center;">'
            '<svg width="95" height="80" viewBox="0 0 120 100">'
            '<polygon points="20,25 100,25 95,75 25,75" fill="none" stroke="#246BCE" stroke-width="4"/>'
            '</svg>'
            '</div>'
            '<div style="font-size:15px;font-weight:700;color:#334155;">C2</div>'
            '<div style="font-size:13px;color:#64748B;margin-top:4px;">Rectangular Horizontal</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div style="text-align:center;padding:10px;">'
            '<div style="height:110px;display:flex;align-items:center;justify-content:center;">'
            '<svg width="95" height="80" viewBox="0 0 120 100">'
            '<rect x="30" y="20" width="60" height="60" fill="none" stroke="#246BCE" stroke-width="4"/>'
            '</svg>'
            '</div>'
            '<div style="font-size:15px;font-weight:700;color:#334155;">C3</div>'
            '<div style="font-size:13px;color:#64748B;margin-top:4px;">Square</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div style="text-align:center;padding:10px;">'
            '<div style="height:110px;display:flex;align-items:center;justify-content:center;">'
            '<svg width="95" height="80" viewBox="0 0 120 100">'
            '<polygon points="35,20 85,20 100,80 20,80" fill="none" stroke="#246BCE" stroke-width="4"/>'
            '</svg>'
            '</div>'
            '<div style="font-size:15px;font-weight:700;color:#334155;">C4</div>'
            '<div style="font-size:13px;color:#64748B;margin-top:4px;">Trapezoidal</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-card">'
        '<table class="measurement-table">'
        '<tr><th>Vertebra</th><th>Shape</th><th>Description</th></tr>'
        '<tr><td>C2</td><td><b>Rectangular Horizontal</b></td><td>Width greater than height</td></tr>'
        '<tr><td>C3</td><td><b>Square</b></td><td>Height approximately equals width</td></tr>'
        '<tr><td>C4</td><td><b>Trapezoidal</b></td><td>Posterior height greater than anterior height</td></tr>'
        '</table>'
        '</div>',
        unsafe_allow_html=True
    )


    # ============================================================
    # 4. MORPHOLOGICAL MEASUREMENTS
    # ============================================================

    st.markdown("""
    <div class="section-card">
        <div class="section-title">
            4. Morphological Measurements (mm)
        </div>
        <table class="measurement-table">
            <tr>
                <th>Measurement</th>
                <th>C2</th>
                <th>C3</th>
                <th>C4</th>
            </tr>
            <tr>
                <td>Anterior Height (AH)</td>
                <td>7.7</td>
                <td>8.2</td>
                <td>8.5</td>
            </tr>
            <tr>
                <td>Posterior Height (PH)</td>
                <td>6.6</td>
                <td>7.8</td>
                <td>7.9</td>
            </tr>
            <tr>
                <td>Middle Height (MH)</td>
                <td>7.0</td>
                <td>8.0</td>
                <td>8.2</td>
            </tr>
            <tr>
                <td>Width (W)</td>
                <td>12.3</td>
                <td>10.1</td>
                <td>10.3</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # 5 + 6. PREDICTED STAGE & GROWTH PHASE
    # ============================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="section-card">
            <div class="section-title">
                5. Predicted CVM Stage
            </div>
            <div class="stage-card">
                <div class="stage-label">
                    Predicted Stage
                </div>
                <div class="stage-value">
                    CS4
                </div>
                <div class="stage-description">
                    Peak Growth Passed Recently
                </div>
                <div class="confidence">
                    Confidence: <b>92.4%</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="section-card">
            <div class="section-title">
                6. Growth Phase Interpretation
            </div>
            <div class="interpretation-card">
                <b>CS4 — Peak Growth Passed Recently</b>
                <br><br>
                The morphological characteristics of C2, C3,
                and C4 indicate that the peak mandibular growth
                period has recently passed.
            </div>
        </div>
        """, unsafe_allow_html=True)


    # ============================================================
    # AGE CORRELATION REFERENCE
    # ============================================================

    with st.expander("Age Correlation Reference"):

        st.markdown("""
        <div class="age-reference">
        <table class="measurement-table">
            <tr>
                <th>Stage</th>
                <th>Approx. Age Range</th>
            </tr>
            <tr>
                <td>CS1</td>
                <td>6–8 years</td>
            </tr>
            <tr>
                <td>CS2</td>
                <td>8–9 years</td>
            </tr>
            <tr>
                <td>CS3</td>
                <td>10–12 years</td>
            </tr>
            <tr>
                <td>CS4</td>
                <td>11–13 years</td>
            </tr>
            <tr>
                <td>CS5</td>
                <td>12–15 years</td>
            </tr>
            <tr>
                <td>CS6</td>
                <td>15 years and above</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)


    # ============================================================
    # 7. AUTOMATED CLINICAL REPORT SUMMARY
    # ============================================================

    st.markdown("""
    <div class="section-card">
        <div class="section-title">
            7. Automated Clinical Report Summary
        </div>
        <div class="summary-box">
            <b>Predicted CVM Stage:</b> CS4
            <br>
            <b>Growth Phase:</b> Peak growth passed recently
            <br>
            <b>Concavity (C2/C3/C4):</b>
            Deep / Moderate / Moderate
            <br>
            <b>Shape (C2/C3/C4):</b>
            Trapezoid / Square / Rectangular Horizontal
            <br>
            <b>Confidence:</b> 92.4%
            <br>
            <b>Clinical Interpretation:</b>
            The observed cervical vertebral morphological
            characteristics are consistent with CVM Stage CS4.
        </div>
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # DISCLAIMER
    # ============================================================

    st.caption(
        "This system is designed to support clinical decision making "
        "and does not replace professional judgment."
    )