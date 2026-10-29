
import cv2
import numpy as np


def estimate_concavity(vertebra_crop):
    """
    Estimate inferior-border concavity using image processing.
    Returns depth in pixels and a prototype classification.
    """

    if vertebra_crop is None or vertebra_crop.size == 0:
        return {
            "depth_px": None,
            "classification": "Unable to Analyse"
        }

    gray = cv2.cvtColor(vertebra_crop, cv2.COLOR_RGB2GRAY)
    height, width = gray.shape

    if height < 20 or width < 20:
        return {
            "depth_px": None,
            "classification": "Unable to Analyse"
        }

    gray = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    ).apply(gray)

    start_y = int(height * 0.55)
    end_y = int(height * 0.95)
    lower = gray[start_y:end_y, :]

    gradient = np.abs(
        cv2.Sobel(lower, cv2.CV_32F, 0, 1, ksize=3)
    )

    border_positions = []

    for x in range(width):
        column = gradient[:, x]

        if column.size == 0:
            border_positions.append(np.nan)
            continue

        y = int(np.argmax(column))
        strength = float(column[y])

        if strength < 8:
            border_positions.append(np.nan)
        else:
            border_positions.append(start_y + y)

    profile = np.array(border_positions, dtype=float)
    valid_ratio = np.isfinite(profile).mean()

    if valid_ratio < 0.70:
        return {
            "depth_px": None,
            "classification": "Unable to Analyse"
        }

    valid = np.isfinite(profile)

    profile = np.interp(
        np.arange(width),
        np.flatnonzero(valid),
        profile[valid]
    )

    window = max(3, int(width * 0.05))

    if window % 2 == 0:
        window += 1

    if window >= width:
        window = width - 1 if width % 2 == 0 else width

    if window >= 3:
        kernel = np.ones(window, dtype=float) / window
        profile = np.convolve(
            profile,
            kernel,
            mode="same"
        )

    side_width = max(2, int(width * 0.15))
    centre_start = int(width * 0.40)
    centre_end = int(width * 0.60)

    side_positions = np.concatenate([
        profile[:side_width],
        profile[-side_width:]
    ])

    centre_positions = profile[centre_start:centre_end]

    if len(centre_positions) == 0:
        return {
            "depth_px": None,
            "classification": "Unable to Analyse"
        }

    side_level = float(np.median(side_positions))
    centre_level = float(np.median(centre_positions))

    depth_px = side_level - centre_level

    if not np.isfinite(depth_px):
        return {
            "depth_px": None,
            "classification": "Unable to Analyse"
        }

    depth_px = round(max(0.0, depth_px), 2)

    # Experimental thresholds; not clinically validated.
    if depth_px < 1.0:
        classification = "Flat"
    elif depth_px < 3.0:
        classification = "Slight Concavity"
    elif depth_px < 5.0:
        classification = "Moderate Concavity"
    else:
        classification = "Deep Concavity"

    return {
        "depth_px": depth_px,
        "classification": classification
    }
