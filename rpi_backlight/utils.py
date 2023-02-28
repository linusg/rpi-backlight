from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from __init__ import BoardType

__all__ = ["detect_board_type", "FakeBacklightSysfs"]


def detect_board_type() -> Optional["BoardType"]:
    """Try to detect the board type based on the model string in
    ``/proc/device-tree/model``.
    """

    from . import BoardType

    model_file = Path("/proc/device-tree/model")
    try:
        model = model_file.read_text()
    except OSError:
        return None
    # Tinker Board 2/2S starts with ASUS Tinker Board 2 or ASUS Tinker Board 2S
    if "Tinker Board 2" in model:
        return BoardType.TINKER_BOARD_2
    # Tinker Board 1/1S starts with Rockchip RK3288 Asus Tinker Board or Rockchip RK3288 Asus Tinker Board S
    elif "Tinker Board" in model:
        return BoardType.TINKER_BOARD
    # Raspberry Pi starts with Raspberry Pi
    elif "Raspberry Pi" in model:
        return BoardType.RASPBERRY_PI
    # Microsoft Surface RT starts with Microsoft Surface RT
    elif "Microsoft Surface RT" in model:
        return BoardType.MICROSOFT_SURFACE_RT
    else:
        return None


class FakeBacklightSysfs:
    """Context manager to create a temporary "fake sysfs" containing all relevant files.
    Used for tests and emulation.

    >>> with FakeBacklightSysfs() as backlight_sysfs:
    ...     backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)
    ...     # use `backlight` as usual
    """

    def __init__(self) -> None:
        self._temp_dir = TemporaryDirectory()
        self.path = Path(self._temp_dir.name)

    def __enter__(self) -> "FakeBacklightSysfs":
        files = {"bl_power": 0, "brightness": 255, "max_brightness": 255}
        for filename, value in files.items():
            (self.path / filename).write_text(str(value))
        Path(self.path / "actual_brightness").symlink_to(self.path / "brightness")
        return self

    def __exit__(self, *_) -> None:
        self._temp_dir.cleanup()
