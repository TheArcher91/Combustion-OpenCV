I have added the scripts for (i) Flame Length and blue to yellow flame region ratio calculator script (ii) plotter of droplet combustion experiment.


# Vision-Based Flame Structure Analysis

This repository contains a Python–OpenCV pipeline developed to **quantitatively analyze flame structure from combustion video data**. The objective of this code is to extract physically meaningful metrics from raw visual inputs using computer vision techniques.

The script processes flame videos captured through an optical window and computes:
- **Average flame length** in real-world units (cm) using pixel-to-physical calibration.
- **Yellow-to-blue flame area ratio**, serving as a proxy for soot formation and combustion regime identification.

The pipeline leverages **HSV color-space segmentation** to isolate flame regions, extracts dominant flame contours, and performs frame-wise aggregation to obtain statistically robust average metrics. These visual features can be correlated with operating parameters such as **fuel flow rate, equivalence ratio, and exit temperature** to study flame stability and combustion behavior.

This work demonstrates the use of computer vision for **structured analysis of dynamic physical phenomena**, with emphasis on:
- Video-based feature extraction
- Geometric measurement from images
- Color-based region classification
- Reproducible and scalable analysis pipelines

The methodology and implementation are directly applicable to broader domains involving **visual data interpretation, physical calibration, and quantitative analysis**, including vision-driven scientific computing and rendering pipelines.
