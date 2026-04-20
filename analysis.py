# analysis.py
# FWHM Analysis — Z-Scan Intensity Data
# Loads saved scan data, fits a UnivariateSpline, and computes
# Full Width at Half-Maximum (FWHM) for both Forward and Backward scans.

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


def compute_fwhm(positions, intensities, label, color):
    """
    Fit a spline to the intensity profile and compute its FWHM.

    The spline is evaluated on a fine grid to achieve sub-micron
    accuracy — important because the true focus peak often falls
    between the 0.02 mm discrete measurement steps.

    Args:
        positions (np.ndarray): Z-positions in mm.
        intensities (np.ndarray): Maximum pixel intensities at each position.
        label (str): Scan label for plot legend (e.g. 'Forward').
        color (str): Line color for the plot.

    Returns:
        float: Estimated FWHM in millimetres.
    """
    # Fit spline to raw data
    spline = UnivariateSpline(positions, intensities - np.max(intensities) / 2, s=0)

    # Find roots (half-maximum crossings)
    roots = spline.roots()

    if len(roots) >= 2:
        fwhm = roots[-1] - roots[0]
    else:
        fwhm = float("nan")
        print(f"[WARNING] Could not find two half-maximum crossings for {label} scan.")

    # Fine grid for smooth curve
    z_fine = np.linspace(positions[0], positions[-1], 2000)
    intensity_fine = UnivariateSpline(positions, intensities, s=0)(z_fine)

    # Plot raw data and fitted curve
    plt.scatter(positions, intensities, color=color, alpha=0.4, s=15, label=f"{label} (raw)")
    plt.plot(z_fine, intensity_fine, color=color, linewidth=2, label=f"{label} (spline fit)")

    # Annotate FWHM
    half_max = np.max(intensities) / 2
    if not np.isnan(fwhm):
        plt.annotate(
            f"FWHM = {fwhm:.4f} mm",
            xy=(roots[0] + fwhm / 2, half_max),
            xytext=(roots[0] + fwhm / 2, half_max * 1.15),
            ha="center", fontsize=9, color=color,
            arrowprops=dict(arrowstyle="-", color=color, lw=1)
        )

    return fwhm


def main():
    # Load saved scan data
    data_file = "results/intensity_data.npz"
    try:
        data = np.load(data_file)
    except FileNotFoundError:
        print(f"[ERROR] Data file not found: '{data_file}'")
        print("  Please run zscan.py first to generate scan data.")
        return

    pos_fwd   = data["positions_fwd"]
    int_fwd   = data["intensities_fwd"]
    pos_bwd   = data["positions_bwd"]
    int_bwd   = data["intensities_bwd"]

    # ── Plot ──────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.sca(ax)

    fwhm_fwd = compute_fwhm(pos_fwd, int_fwd, label="Forward",  color="#1f77b4")
    fwhm_bwd = compute_fwhm(pos_bwd, int_bwd, label="Backward", color="#d62728")

    # Half-maximum reference line
    overall_half_max = max(np.max(int_fwd), np.max(int_bwd)) / 2
    plt.axhline(overall_half_max, color="gray", linestyle="--", linewidth=1, label="Half Maximum")

    # Labels and formatting
    plt.xlabel("Z Position (mm)", fontsize=12)
    plt.ylabel("Maximum Pixel Intensity (a.u.)", fontsize=12)
    plt.title("Z-Scan: Maximum Intensity vs. Z-Position\n(Forward & Backward — Hysteresis Analysis)", fontsize=13)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save and display
    output_path = "results/zscan_plot.png"
    plt.savefig(output_path, dpi=150)
    print(f"\n[Results] Plot saved to '{output_path}'")
    print(f"  Forward  FWHM : {fwhm_fwd:.4f} mm")
    print(f"  Backward FWHM : {fwhm_bwd:.4f} mm")

    plt.show()


if __name__ == "__main__":
    main()
