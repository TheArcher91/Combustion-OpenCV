import cv2
import numpy as np
import argparse

# -----------------------------
# USER-DEFINED PARAMETERS
# -----------------------------
OPTICAL_WINDOW_HEIGHT_CM = 64.0   # physical height of optical window
MIN_CONTOUR_AREA = 500            # noise threshold (tunable)

# HSV ranges (tunable based on lighting)
YELLOW_LOWER = np.array([20, 100, 100])
YELLOW_UPPER = np.array([40, 255, 255])

BLUE_LOWER = np.array([100, 150, 50])
BLUE_UPPER = np.array([130, 255, 255])


# -----------------------------
# CORE PROCESSING FUNCTION
# -----------------------------
def analyze_flame_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise IOError("Could not open video file.")

    # Read first frame for calibration
    ret, first_frame = cap.read()
    if not ret:
        raise IOError("Could not read first frame.")

    frame_height_px = first_frame.shape[0]
    cm_per_pixel = OPTICAL_WINDOW_HEIGHT_CM / frame_height_px

    # Reset video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    total_flame_length_px = 0.0
    yellow_area_total = 0
    blue_area_total = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Color segmentation
        yellow_mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)
        blue_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)

        yellow_area = cv2.countNonZero(yellow_mask)
        blue_area = cv2.countNonZero(blue_mask)

        # Combined flame mask
        flame_mask = cv2.bitwise_or(yellow_mask, blue_mask)

        # Find flame contour
        contours, _ = cv2.findContours(
            flame_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > MIN_CONTOUR_AREA:
                x, y, w, h = cv2.boundingRect(largest_contour)
                total_flame_length_px += h

        yellow_area_total += yellow_area
        blue_area_total += blue_area

    cap.release()

    # Compute final metrics
    avg_flame_length_px = total_flame_length_px / frame_count
    avg_flame_length_cm = avg_flame_length_px * cm_per_pixel

    yellow_blue_ratio = (
        yellow_area_total / blue_area_total if blue_area_total > 0 else np.inf
    )

    return avg_flame_length_cm, yellow_blue_ratio


# -----------------------------
# MAIN ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vision-based flame structure analysis using OpenCV"
    )
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to flame video file"
    )

    args = parser.parse_args()

    avg_length_cm, yb_ratio = analyze_flame_video(args.video)

    print("\n--- Flame Analysis Results ---")
    print(f"Average Flame Length      : {avg_length_cm:.2f} cm")
    print(f"Yellow-to-Blue Area Ratio : {yb_ratio:.2f}")
