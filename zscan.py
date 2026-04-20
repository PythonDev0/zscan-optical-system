# zscan.py
# Main Experiment Script — Automated Z-Scan
# Performs a forward and backward scan, captures images at each step,
# and saves maximum intensity data for FWHM analysis.

import os
import numpy as np
from PIL import Image
from camera import ThorlabsCamera
from stage import AerotechStage

# ─────────────────────────────────────────────
# Experiment Parameters
# ─────────────────────────────────────────────
SCAN_START_MM   = -1.0
SCAN_END_MM     =  1.0
STEP_SIZE_MM    =  0.02
STAGE_SPEED     =  1.0    # mm/s

OUTPUT_DIR_FWD  = "results/forward"
OUTPUT_DIR_BWD  = "results/backward"
DATA_FILE       = "results/intensity_data.npz"


def run_scan(stage, camera, positions, output_dir, label):
    """
    Execute a single directional scan (forward or backward).

    Args:
        stage (AerotechStage): Initialized stage object.
        camera (ThorlabsCamera): Initialized camera object.
        positions (np.ndarray): Array of Z positions in mm.
        output_dir (str): Folder path to save captured images.
        label (str): Human-readable scan label for console output.

    Returns:
        list[float]: Maximum pixel intensity at each position.
    """
    os.makedirs(output_dir, exist_ok=True)
    intensities = []

    print(f"\n[Scan] Starting {label} scan — {len(positions)} steps")

    for i, z in enumerate(positions):
        # 1. Move stage to target position (blocking)
        stage.move_absolute(z, STAGE_SPEED)

        # 2. Capture image
        img = camera.capture_image()

        # 3. Extract maximum intensity
        max_intensity = np.max(img)
        intensities.append(max_intensity)

        # 4. Save image
        filename = os.path.join(output_dir, f"z_{z:+.3f}mm.png")
        Image.fromarray(img).save(filename)

        print(f"  Step {i+1:03d}/{len(positions)} | Z = {z:+.3f} mm | Max intensity = {max_intensity}")

    print(f"[Scan] {label} scan complete.")
    return intensities


def main():
    # Generate scan positions
    pos_forward  = np.arange(SCAN_START_MM, SCAN_END_MM + STEP_SIZE_MM, STEP_SIZE_MM)
    pos_backward = pos_forward[::-1]

    stage  = None
    camera = None

    try:
        # Initialize hardware
        camera = ThorlabsCamera(device_id=0)
        stage  = AerotechStage(axis_name="Z")

        # Run forward scan
        intensities_fwd = run_scan(
            stage, camera, pos_forward, OUTPUT_DIR_FWD, label="Forward"
        )

        # Run backward scan
        intensities_bwd = run_scan(
            stage, camera, pos_backward, OUTPUT_DIR_BWD, label="Backward"
        )

        # Save intensity data for analysis
        os.makedirs("results", exist_ok=True)
        np.savez(
            DATA_FILE,
            positions_fwd  = pos_forward,
            intensities_fwd= np.array(intensities_fwd),
            positions_bwd  = pos_backward,
            intensities_bwd= np.array(intensities_bwd)
        )
        print(f"\n[Data] Intensity data saved to '{DATA_FILE}'")
        print("[Done] Z-scan experiment complete. Run analysis.py to compute FWHM.")

    except Exception as e:
        print(f"\n[ERROR] Experiment aborted: {e}")

    finally:
        if camera:
            camera.release()
        if stage:
            stage.disable()


if __name__ == "__main__":
    main()
