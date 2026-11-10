
"""
CVM lower-border concavity analysis (C2, C3, C4)
on lateral cephalometric radiographs.

Manual landmark selection:
lp = Most posterior point of the lower border
lm = Deepest point of the lower-border concavity
la = Most anterior point of the lower border

Concavity depth = perpendicular distance from lm to lp-la line.
Concavity is PRESENT if depth >= 1 mm.

Run: streamlit run cvm_concavity_app.py
"""

from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import (streamlit_image_coordinates)

NAMES = ["C2", "C3", "C4"]
LM_ORDER = [f"{v}{p}" for v in NAMES for p in ("lp", "lm", "la")]

LM_HELP = {
    "lp": "most POSTERIOR point of the lower border",
    "lm": "DEEPEST point of the concavity (or middle of the border if flat)",
    "la": "most ANTERIOR point of the lower border"
}


# --------------------------------------------------------------------------- #
# Core analysis
# --------------------------------------------------------------------------- #

@dataclass
class VertebraResult:
    name: str
    box: Optional[tuple]
    border: np.ndarray
    p_post: tuple
    p_ant: tuple
    deepest: tuple
    foot: tuple
    depth_px: float
    depth_mm: float
    concave: bool


def to_uint8_gray(img: np.ndarray) -> np.ndarray:
    if img.ndim == 3:
        img = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2GRAY)

    if img.dtype != np.uint8:
        img = cv2.normalize(
            img.astype(np.float32),
            None, 0, 255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

    return img


def result_from_landmarks(
    name, lp, lm, la, pixel_mm, threshold_mm=1.0,
    border=None, box=None
) -> VertebraResult:

    """Calculate concavity depth using the three selected landmarks."""

    p1, p2, pm = (
        np.asarray(p, float) for p in (lp, la, lm)
    )

    d = p2 - p1
    L = float(np.linalg.norm(d))

    if L < 1e-6:
        raise ValueError(f"{name}: lp and la are the same point.")

    n = np.array([-d[1], d[0]]) / L

    # Normal pointing upward into the vertebral body.
    if n[1] > 0:
        n = -n

    depth_px = max(float((pm - p1) @ n), 0.0)

    foot = p1 + ((pm - p1) @ d / L ** 2) * d

    depth_mm = depth_px * pixel_mm

    if border is None:
        border = np.array([p1, pm, p2])

    return VertebraResult(
        name,
        box,
        np.asarray(border, float),
        tuple(p1),
        tuple(p2),
        tuple(pm),
        tuple(foot),
        depth_px,
        depth_mm,
        depth_mm >= threshold_mm
    )


def suggest_cvm_stage(results) -> str:

    c = {r.name: r.concave for r in results}

    if not all(k in c for k in NAMES):
        return "Need C2, C3 and C4 to suggest a stage."

    if c["C2"] and c["C3"] and c["C4"]:
        return (
            "CS4-CS6 (concavity in C2, C3 and C4; "
            "body shape needed to separate them)"
        )

    if c["C2"] and c["C3"]:
        return "CS3 (concavity in C2 and C3 only)"

    if c["C2"] and not c["C3"] and not c["C4"]:
        return "CS2 (concavity in C2 only)"

    if not any(c.values()):
        return "CS1 (no concavity)"

    return "Pattern does not match Table 4 - check the landmarks."


def draw_results(gray, results, threshold_mm=1.0) -> np.ndarray:

    out = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    s = max(out.shape[:2]) / 1000.0
    th = max(1, int(round(2 * s)))
    fs = 0.45 * s + 0.15

    pt = lambda p: (
        int(round(p[0])),
        int(round(p[1]))
    )

    for r in results:

        col = (0, 0, 255) if r.concave else (0, 200, 0)

        cv2.polylines(
            out,
            [r.border.astype(np.int32).reshape(-1, 1, 2)],
            False,
            (255, 255, 0),
            th
        )

        # Line joining lp and la.
        cv2.line(
            out,
            pt(r.p_post),
            pt(r.p_ant),
            (0, 255, 255),
            th
        )

        # Mark lp and la.
        for p, lab in (
            (r.p_post, "lp"),
            (r.p_ant, "la")
        ):
            cv2.circle(
                out,
                pt(p),
                int(4 * s) + 1,
                (255, 0, 255),
                -1
            )

            cv2.putText(
                out,
                f"{r.name}{lab}",
                (
                    pt(p)[0] - int(10 * s),
                    pt(p)[1] + int(18 * s)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                fs,
                (255, 0, 255),
                1,
                cv2.LINE_AA
            )

        # Concavity depth line.
        if r.depth_px > 0:
            cv2.line(
                out,
                pt(r.foot),
                pt(r.deepest),
                col,
                th
            )

        # Mark lm.
        cv2.circle(
            out,
            pt(r.deepest),
            int(5 * s) + 2,
            col,
            -1
        )

        cv2.putText(
            out,
            f"{r.name}lm",
            (
                pt(r.deepest)[0] - int(10 * s),
                pt(r.deepest)[1] - int(8 * s)
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            fs,
            col,
            1,
            cv2.LINE_AA
        )

        # Depth label.
        label = (
            f"{r.name}: {r.depth_mm:.2f} mm "
            f"{'present' if r.concave else 'absent'}"
        )

        anchor = max(r.p_post[0], r.p_ant[0])

        cv2.putText(
            out,
            label,
            (
                int(anchor) + int(12 * s),
                pt(r.deepest)[1]
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            fs * 1.2,
            col,
            th,
            cv2.LINE_AA
        )

    return out


# --------------------------------------------------------------------------- #
# Streamlit UI
# --------------------------------------------------------------------------- #

def show_manual_analysis(uploaded_xray):

    st.title("CVM lower-border concavity (C2-C4)")

    if uploaded_xray is None:
        st.warning("No X-ray image available.")
        return

    # Read uploaded image
    uploaded_xray.seek(0)

    raw = cv2.imdecode(
        np.frombuffer(uploaded_xray.getvalue(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )

    if raw is None:
        st.error("Could not read the image.")
        return

    gray = to_uint8_gray(raw)

    # ---------------------------------------------------------
    # Session state
    # ---------------------------------------------------------

    if "manual_pts" not in st.session_state:
        st.session_state.manual_pts = {}

    if "manual_last_click" not in st.session_state:
        st.session_state.manual_last_click = None

    if "manual_sig" not in st.session_state:
        st.session_state.manual_sig = None

    # Reset when a different image is uploaded
    import hashlib

    sig = hashlib.md5(
        uploaded_xray.getvalue()
    ).hexdigest()

    if st.session_state.manual_sig != sig:
        st.session_state.manual_sig = sig
        st.session_state.manual_pts = {}
        st.session_state.manual_last_click = None

    pts = st.session_state.manual_pts

    # ---------------------------------------------------------
    # Image preparation
    # ---------------------------------------------------------

    H, W = gray.shape

    k = max(1.0, 1000.0 / max(H, W))

    work = cv2.resize(
        gray,
        None,
        fx=k,
        fy=k,
        interpolation=cv2.INTER_CUBIC
    )

    WH, WW = work.shape

    pixel_mm = 0.10
    mm_w = pixel_mm / k
    thr = 1.0

    # ---------------------------------------------------------
    # Manual landmark selection
    # ---------------------------------------------------------

    nxt = next(
        (n for n in LM_ORDER if n not in pts),
        None
    )

    bar = st.columns([3, 1, 1])

    if nxt:
        bar[0].markdown(
            f"**Click `{nxt}`** - {LM_HELP[nxt[-2:]]}"
        )
    else:
        bar[0].success(
            "All 9 landmarks placed. Use Undo to correct."
        )

    if bar[1].button("Undo last", use_container_width=True) and pts:

        last = [
            n for n in LM_ORDER if n in pts
        ][-1]

        pts.pop(last)
        st.session_state.manual_last_click = None
        st.rerun()

    if bar[2].button("Reset", use_container_width=True):

        st.session_state.manual_pts = {}
        st.session_state.manual_last_click = None
        st.rerun()

    # ---------------------------------------------------------
    # Calculate results
    # ---------------------------------------------------------

    results = []
    errors = []

    for v in NAMES:

        if all(
            f"{v}{p}" in pts
            for p in ("lp", "lm", "la")
        ):

            try:
                results.append(
                    result_from_landmarks(
                        v,
                        pts[f"{v}lp"],
                        pts[f"{v}lm"],
                        pts[f"{v}la"],
                        mm_w,
                        thr
                    )
                )

            except ValueError as e:
                errors.append(str(e))

    # ---------------------------------------------------------
    # Image display
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    DISPLAY_WIDTH = 700
    DISPLAY_HEIGHT = 700

    with col1:
        st.subheader("Select Landmarks")

        canvas = cv2.cvtColor(work, cv2.COLOR_GRAY2BGR)

        for n, p in pts.items():
            cv2.circle(canvas, (int(p[0]), int(p[1])), 4, (255, 0, 255), -1)
            cv2.putText(
                canvas, n,
                (int(p[0]) + 6, int(p[1]) - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, cv2.LINE_AA
            )

        display_image = cv2.resize(
            canvas,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

        click = streamlit_image_coordinates(
            Image.fromarray(
                cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            ),
            key="manual_clicker"
        )

        if click and nxt and (
            click["x"], click["y"]
        ) != st.session_state.manual_last_click:

            st.session_state.manual_last_click = (
                click["x"], click["y"]
            )

            sx = WW / DISPLAY_WIDTH
            sy = WH / DISPLAY_HEIGHT

            pts[nxt] = (
                click["x"] * sx,
                click["y"] * sy
            )

            st.rerun()

    with col2:
        st.subheader("Annotated Image")

        annotated = draw_results(work, results, thr)

        annotated_display = cv2.resize(
            annotated,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

        st.image(
            cv2.cvtColor(annotated_display, cv2.COLOR_BGR2RGB),
            width=DISPLAY_WIDTH
        )

    # ---------------------------------------------------------
    # Results and Next button
    # ---------------------------------------------------------

    for e in errors:
        st.warning(e)

    if len(results) == 3 and not errors:

        st.divider()

        st.subheader("Concavity Results")

        st.table([
            {
                "Vertebra": r.name,
                "Depth (px)": round(r.depth_px, 2),
                "Depth (mm)": round(r.depth_mm, 2),
                "Classification": (
                    "Present" if r.concave else "Absent"
                )
            }
            for r in results
        ])

        st.info(
            f"Concavity-based CVM hint: "
            f"{suggest_cvm_stage(results)}"
        )

        if st.button("Next", type="primary"):
            st.session_state["manual_concavity_results"] = [
                {
                    "vertebra": f"CV{r.name[-1]}",
                    "depth_px": r.depth_px,
                    "depth_mm": r.depth_mm,
                    "classification": (
                        "Present" if r.concave else "Absent"
                    )
                }
                for r in results
            ]

            st.session_state["manual_concavity_image"] = annotated

            st.session_state["show_results"] = True
            st.session_state["page"] = "CVM Assessment"

            st.rerun()
