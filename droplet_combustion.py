import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
image_dir = "D:/TetradecaneT1_543"  # <- Update if needed
start_idx = 0
end_idx = 17976  # Inclusive
fps = 4000
line_width_mm = 0.2  # Width of dark line in mm (reference)

# --- FUNCTIONS ---
def process_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Crop to top 60%
    height = int(img.shape[0] * 0.6)
    img_cropped = img[:height, :]

    # Threshold to binary image
    _, binary = cv2.threshold(img_cropped, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological operations to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    binary_cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(binary_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Use vertical diameter only
    vertical_pixels = h

    # Estimate pixel-to-mm ratio using the reference line width
    ref_line_pixel_width = estimate_line_width(binary_cleaned)
    if ref_line_pixel_width == 0:
        return None
    pixel_to_mm = line_width_mm / ref_line_pixel_width

    vertical_diameter_mm = vertical_pixels * pixel_to_mm
    return vertical_diameter_mm

def estimate_line_width(binary_img):
    middle_row = binary_img.shape[0] // 2
    horizontal_profile = binary_img[middle_row, :]
    line_pixels = np.where(horizontal_profile > 0)[0]
    if len(line_pixels) < 2:
        return 0
    widths = np.diff(np.where(np.diff(np.concatenate(([0], horizontal_profile > 0, [0]))) == 1)[0])[::2]
    if len(widths) == 0:
        return 0
    return np.median(widths)

# --- MAIN PROCESSING LOOP ---
diameters = []
times = []

for idx in range(start_idx, end_idx + 1):
    filename = f"Img{idx:06d}.tif"
    path = os.path.join(image_dir, filename)
    d = process_image(path)
    if d is not None:
        diameters.append(d)
        times.append(idx / fps)

# Convert to NumPy arrays
diameters = np.array(diameters)
diameters_squared = diameters ** 2
times = np.array(times)

# --- PLOTTING ---
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(times, diameters, color='blue')
plt.xlabel("Time (s)")
plt.ylabel("Diameter (mm)")
plt.title("Droplet Diameter vs Time")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(times, diameters_squared, color='green')
plt.xlabel("Time (s)")
plt.ylabel("Diameter² (mm²)")
plt.title("Droplet Diameter² vs Time")
plt.grid(True)

plt.tight_layout()
plt.show()
