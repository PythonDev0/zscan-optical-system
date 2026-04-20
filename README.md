# Automated Z-Scan & Optical Calibration System
### Python Interface for Thorlabs Cameras & Aerotech Nanopositioners

> Developed by **Shazib Ullah** — January 2026

---

## Overview

This project automates a Z-scan optical experiment by synchronizing a **Thorlabs DCC1545M camera** with an **Aerotech ANT130LZ nanopositioner** via Python. The system performs bidirectional scans, captures images at each position, and computes the **Full Width at Half-Maximum (FWHM)** of the intensity profile using spline interpolation.

---

## Hardware

| Component | Device | Driver |
|-----------|--------|--------|
| Camera | Thorlabs DCC1545M (CMOS Monochrome, 1280×1024) | `pyueye` (uEye SDK) |
| Stage | Aerotech ANT130LZ (Z-Axis Nanopositioner) | `automation1` Python API |
| Interface | USB — PC acts as central sync unit | — |

---

## Software Architecture

The codebase is built on three core principles:

1. **Modular OOP Design** — `Camera` and `Stage` are independent classes, making hardware replacement straightforward without touching the experiment logic.
2. **Blocking Sequential Execution** — The stage must fully settle before the camera triggers, preventing motion blur and ensuring positional accuracy.
3. **Robust Error Handling** — `try...except` blocks catch missing drivers or disconnected hardware gracefully.

---

## Repository Structure

```
zscan-optical-system/
│
├── README.md
│
├── src/
│   ├── camera.py          # ThorlabsCamera class — memory allocation & image capture
│   ├── stage.py           # AerotechStage class — motion control & blocking commands
│   ├── zscan.py           # Main experiment loop — forward & backward scan
│   └── analysis.py        # FWHM calculation via scipy spline interpolation
│
├── results/
│   └── zscan_plot.png     # Forward vs Backward intensity plot (generated output)
│
├── docs/
│   └── presentation.pdf   # Full project presentation slides
│
├── requirements.txt
└── .gitignore
```

---

## Experiment Protocol

### Scan Parameters
- **Range:** −1.0 mm to +1.0 mm
- **Step Size:** 0.02 mm (100 steps per direction)
- **Total Positions:** 200 (100 forward + 100 backward)

### Procedure
1. **Forward Scan** — Stage moves from −1.0 mm → +1.0 mm, capturing one image per step
2. **Backward Scan** — Stage returns from +1.0 mm → −1.0 mm, capturing one image per step
3. **Analysis** — Maximum pixel intensity is extracted from each image and plotted vs. Z-position
4. **FWHM** — A `UnivariateSpline` from `scipy` fits the intensity curve for sub-micron accuracy

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/zscan-optical-system.git
cd zscan-optical-system

# Install dependencies
pip install -r requirements.txt
```

> **Note:** `pyueye` requires the IDS uEye SDK to be installed on your system.  
> `automation1` requires the Aerotech Automation1 controller software.

---

## Usage

```bash
# Run the full Z-scan experiment
python src/zscan.py

# Run analysis only (on existing data)
python src/analysis.py
```

---

## Results

The experiment produces a **hysteresis plot** comparing Forward and Backward scans:

- 🔵 **Blue line** — Forward scan (−1.0 mm → +1.0 mm)
- 🔴 **Red line** — Backward scan (+1.0 mm → −1.0 mm)

FWHM values are printed to the console and annotated on the plot.

---

## Dependencies

See `requirements.txt`:

```
numpy
scipy
matplotlib
pyueye
automation1
```

---

## Presentation

The full project presentation is available in [`docs/presentation.pdf`](docs/presentation.pdf).

---

## Author

**Shazib Ullah**  
Automated Z-Scan Control System — January 2026
