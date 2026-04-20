# camera.py
# Thorlabs DCC1545M Camera Interface
# Manages uEye SDK initialization, memory allocation, and image capture.

from pyueye import ueye
import numpy as np


class ThorlabsCamera:
    """
    Interface for the Thorlabs DCC1545M CMOS monochrome camera.

    Handles:
        - Camera initialization and color mode configuration
        - Dynamic image memory allocation
        - Single-frame capture (freeze mode)
        - Safe resource release
    """

    def __init__(self, device_id=0):
        """
        Initialize the camera, set Mono8 color mode, and allocate image memory.

        Args:
            device_id (int): uEye device ID (default: 0 for first connected camera)
        """
        self.h_cam = ueye.HIDS(device_id)
        self.width = 1280
        self.height = 1024
        self.mem_ptr = ueye.c_mem_p()
        self.mem_id = ueye.INT()

        try:
            # Initialize camera
            ret = ueye.is_InitCamera(self.h_cam, None)
            if ret != ueye.IS_SUCCESS:
                raise RuntimeError(f"Camera init failed with code {ret}")

            # Set monochrome 8-bit mode
            ueye.is_SetColorMode(self.h_cam, ueye.IS_CM_MONO8)

            # Allocate image memory
            ueye.is_AllocImageMem(
                self.h_cam, self.width, self.height, 8,
                self.mem_ptr, self.mem_id
            )
            ueye.is_SetImageMem(self.h_cam, self.mem_ptr, self.mem_id)

            print(f"[Camera] Initialized — {self.width}x{self.height} Mono8")

        except Exception as e:
            print(f"[Camera] ERROR during initialization: {e}")
            raise

    def capture_image(self):
        """
        Capture a single frozen frame and return it as a NumPy array.

        Returns:
            np.ndarray: 2D array of shape (height, width) with uint8 pixel values.
        """
        ueye.is_FreezeVideo(self.h_cam, ueye.IS_WAIT)

        data = ueye.get_data(
            self.mem_ptr, self.width, self.height, 8, self.width, copy=True
        )
        return np.reshape(data, (self.height, self.width))

    def release(self):
        """Free memory and close the camera connection."""
        ueye.is_FreeImageMem(self.h_cam, self.mem_ptr, self.mem_id)
        ueye.is_ExitCamera(self.h_cam)
        print("[Camera] Released.")
