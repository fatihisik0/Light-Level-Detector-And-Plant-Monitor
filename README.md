# 🔍 Intelligent Light Level Detector & Monitor

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=flat&logo=opencv)
![Matplotlib](https://img.shields.io/badge/Data-Visualization-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Executive Summary
The **Intelligent Light Level Detector** is a computer vision-based software designed to measure, analyze, and track environmental brightness in real-time. Unlike hardware sensors that measure global ambient light, this system utilizes a **Region of Interest (ROI)** mechanism to analyze specific targets within a video feed.

This project bridges the gap between raw data acquisition and actionable insights, making it suitable for engineering applications ranging from **industrial quality control** to **precision agriculture**.

---

## 🚀 Key Features

### 1. Advanced ROI-Based Detection
* **Precision Targeting:** Users can manually select any object or area in the frame to monitor (e.g., a machine part, a workstation, or a plant leaf).
* **Background Isolation:** The algorithm ignores surrounding light changes, focusing strictly on the target area.

### 2. Real-Time Data Analysis
* **Live Metrics:** Instantly calculates the average pixel intensity ($0-255$) of the target.
* **Dynamic Visualization:** Displays a live graph of light fluctuations using `Matplotlib`.
* **HUD System:** Provides immediate visual feedback (Green/Red bounding boxes) based on configurable thresholds.

### 3. Automated Efficiency Reporting
* **Session Analytics:** Upon termination, the system generates a "Performance Report Card."
* **Optimization Metrics:** Tracks "Optimal Condition Duration" versus "Total Elapsed Time" to calculate an efficiency percentage.

---

## 🛠️ Engineering Use Cases
While the core algorithm is a general-purpose light detector, it has been optimized for the following scenarios:

### 🌱 Application A: Precision Agriculture (Primary Demo)
* **Goal:** Monitoring photosynthesis requirements for indoor plants.
* **Function:** The system tracks whether a specific plant receives adequate light duration throughout the day, helping to optimize artificial grow lights.

### 🏭 Application B: Industrial & Ergonomics
* **Goal:** Workplace safety and quality control.
* **Function:** Can be used to ensure assembly lines have consistent lighting or to verify that employee workstations meet OSHA/ISO lighting standards.

### 🎥 Application C: Photography & Studio
* **Goal:** Scene consistency.
* **Function:** detecting unwanted shadows or light intensity drops during long video shoots.

---

## ⚙️ Technical Architecture

The system operates on a 4-step processing pipeline:

1.  **Acquisition:** Captures video frames from a standard webcam via **OpenCV**.
2.  **Preprocessing:** Converts the selected ROI from RGB to **Grayscale** to reduce computational load and isolate luminance.
3.  **Computation:** Calculates the arithmetic mean of pixel intensities within the ROI matrix (`numpy.mean`).
4.  **Decision Logic:** Compares real-time values against a defined threshold (e.g., `Threshold = 90`) to determine the status (IDEAL vs. LOW LIGHT).

---

## 💻 Installation & Usage

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/fatihisik0/Light-Level-Detector-And-Plant-Monitor.git 
    ```

2.  **Install Dependencies:**
    ```bash
    pip install opencv-python numpy matplotlib
    ```

3.  **Run the System:**
    ```bash
    python main.py
    ```

4.  **How to Use:**
    * Launch the app.
    * Draw a box around your target object using the mouse.
    * Press **ENTER** to start monitoring.
    * Press **'q'** to stop and view the analysis report.

---

## 📊 Project Status
* **Current Version:** v2.0 (Stable)
* **Focus:** Real-time optimization and reporting.
* **Developer:** Fatih Işık