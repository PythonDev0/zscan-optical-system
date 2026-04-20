# stage.py
# Aerotech ANT130LZ Nanopositioner Interface
# Wraps the Automation1 Python API into simple, experiment-ready commands.

import time
from automation1 import Controller


class AerotechStage:
    """
    Interface for the Aerotech ANT130LZ Z-axis nanopositioner.

    Wraps the Automation1 API to provide:
        - Simple absolute positioning commands
        - Blocking motion (waits for full mechanical settle)
        - Safe enable/disable of the axis
    """

    def __init__(self, axis_name="Z"):
        """
        Connect to the Aerotech controller and enable the specified axis.

        Args:
            axis_name (str): Axis label as configured in Automation1 (default: 'Z')
        """
        self.axis_name = axis_name

        try:
            self.controller = Controller.connect()
            self.controller.runtime.commands.motion.enable(axis_name)
            print(f"[Stage] Connected — Axis '{axis_name}' enabled.")

        except Exception as e:
            print(f"[Stage] ERROR during connection: {e}")
            raise

    def move_absolute(self, position_mm, speed_mm_per_s=1.0):
        """
        Move the stage to an absolute position and block until motion completes.

        Args:
            position_mm (float): Target position in millimetres.
            speed_mm_per_s (float): Travel speed in mm/s (default: 1.0).
        """
        self.controller.runtime.commands.motion.moveabsolute(
            self.axis_name, [position_mm], speed_mm_per_s
        )
        self.wait_for_motion_done()

    def wait_for_motion_done(self, settling_time_s=0.05):
        """
        Wait for mechanical settling after a move command.

        Args:
            settling_time_s (float): Extra sleep time in seconds after motion (default: 50 ms).
        """
        time.sleep(settling_time_s)

    def get_position(self):
        """
        Query and return the current axis position.

        Returns:
            float: Current position in millimetres.
        """
        return self.controller.runtime.parameters.axes[self.axis_name].PositionFeedback

    def disable(self):
        """Disable the axis and disconnect from the controller."""
        self.controller.runtime.commands.motion.disable(self.axis_name)
        print("[Stage] Axis disabled and controller disconnected.")
