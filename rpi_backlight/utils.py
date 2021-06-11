from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from __init__ import BoardType

__all__ = ["FakeBacklightSysfs"]


def detect_board_type(boardtype: "BoardType") -> Optional[boardtype]:
    model_file = Path("/proc/device-tree/model")
    try:
        model = model_file.read_text()
    except OSError:
        return None
    if model.rfind("Tinker Board 2"):
        return boardtype.TINKER_BOARD_2
    elif model.rfind("Tinker Board"):
        return BoardType.TINKER_BOARD
    elif model.rfind("Raspberry Pi"):
        return BoardType.RASPBERRY_PI
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
