import errno
import time
from contextlib import contextmanager
from enum import Enum
from os import PathLike
from pathlib import Path
from tempfile import gettempdir
from typing import Generator, Union, Optional

from . import utils

__author__ = "Linus Groh"
__version__ = "2.6.0"
__all__ = ["Backlight", "BoardType"]


class BoardType(Enum):
    """Enum to specify a board type in the :class:`~rpi_backlight.Backlight` constructor."""

    #: Raspberry Pi
    RASPBERRY_PI = 1
    #: Tinker Board
    TINKER_BOARD = 2
    #: Tinker Board 2
    TINKER_BOARD_2 = 3
    #: Microsoft Surface RT
    MICROSOFT_SURFACE_RT = 4


_BACKLIGHT_SYSFS_PATHS = {
    BoardType.RASPBERRY_PI: (
        "/sys/class/backlight/10-0045/"
        if Path("/sys/class/backlight/10-0045/").exists()
        else "/sys/class/backlight/rpi_backlight/"
    ),
    BoardType.TINKER_BOARD: "/sys/devices/platform/ff150000.i2c/i2c-3/3-0045/",
    BoardType.TINKER_BOARD_2: "/sys/devices/platform/ff3e0000.i2c/i2c-8/8-0045/",
    BoardType.MICROSOFT_SURFACE_RT: "/sys/class/backlight/backlight/",
}
_EMULATOR_SYSFS_TMP_FILE_PATH = Path(gettempdir()) / "rpi-backlight-emulator.sysfs"
_EMULATOR_MAGIC_STRING = ":emulator:"


def _permission_denied() -> None:
    raise PermissionError(
        "You must either run this program as root or change the permissions "
        "for the backlight access as described in README.md."
    )


class Backlight:
    """Main class to access and control the display backlight power and brightness."""

    def __init__(
        self,
        backlight_sysfs_path: Optional[Union[str, "PathLike[str]"]] = None,
        board_type: BoardType = utils.detect_board_type() or BoardType.RASPBERRY_PI,
    ):
        """Set ``backlight_sysfs_path`` to ``":emulator:"`` to use with rpi-backlight-emulator."""
        if not isinstance(board_type, BoardType):
            raise TypeError(
                f"board_type must be a member of the BoardType enum, got {type(board_type)}"
            )

        if not backlight_sysfs_path:
            backlight_sysfs_path = _BACKLIGHT_SYSFS_PATHS[board_type]
        elif backlight_sysfs_path == _EMULATOR_MAGIC_STRING:
            if not _EMULATOR_SYSFS_TMP_FILE_PATH.exists():
                raise RuntimeError(
                    f"Emulator seems to be not running, {_EMULATOR_SYSFS_TMP_FILE_PATH} not found"
                )
            backlight_sysfs_path = _EMULATOR_SYSFS_TMP_FILE_PATH.read_text()
            # The emulator only knows about Raspberry Pi sysfs files
            # (brightness, bl_power), ignore board_type
            board_type = BoardType.RASPBERRY_PI

        self._backlight_sysfs_path = Path(backlight_sysfs_path)
        self._board_type = board_type
        self._fade_duration = 0.0  # in seconds

        if self._board_type in (BoardType.RASPBERRY_PI, BoardType.MICROSOFT_SURFACE_RT):
            self._max_brightness = self._get_value("max_brightness")  # 255
        elif (
            self._board_type == BoardType.TINKER_BOARD
            or self._board_type == BoardType.TINKER_BOARD_2
        ):
            self._max_brightness = 255

    def _get_value(self, name: str) -> int:
        try:
            return int((self._backlight_sysfs_path / name).read_text())
        except ValueError:
            # Reading failed, sometimes file is empty when updating
            # Try again
            return self._get_value(name)
        except (OSError, IOError) as e:
            if e.errno == errno.EPERM:
                _permission_denied()
            raise e

    def _set_value(self, name: str, value: int) -> None:
        try:
            (self._backlight_sysfs_path / name).write_text(str(value))
        except (OSError, IOError) as e:
            if e.errno == errno.EPERM:
                _permission_denied()
            raise e

    def _normalize_brightness(self, value: float) -> int:
        return max(min(100, int(round(value / self._max_brightness * 100))), 0)

    def _denormalize_brightness(self, value: float) -> int:
        return max(min(255, int(round(value * self._max_brightness / 100))), 0)

    @contextmanager
    def fade(self, duration: float) -> Generator:
        """Context manager for temporarily changing the fade duration.

        >>> backlight = Backlight()
        >>> with backlight.fade(duration=0.5):
        ...     backlight.brightness = 1  # Fade to 100% brightness for 0.5s
        ...
        >>> with backlight.fade(duration=0):
        ...     backlight.brightness = 0  # Set to 0% brightness without fading, use if you have set `backlight.fade_duration` > 0
        """
        old_duration = self.fade_duration
        self.fade_duration = duration
        yield
        self.fade_duration = old_duration

    @property
    def fade_duration(self) -> float:
        """The brightness fade duration in seconds, defaults to 0.
        Also see :meth:`~rpi_backlight.Backlight.fade`.

        >>> backlight = Backlight()
        >>> backlight.fade_duration  # Fading is disabled by default
        0
        >>> backlight.fade_duration = 0.5  # Set to 500ms

        :getter: Return the fade duration.
        :setter: Set the fade duration.
        :type: float
        """
        return self._fade_duration

    @fade_duration.setter
    def fade_duration(self, duration: float) -> None:
        """Set the fade duration."""
        # isinstance(True, int) is True, so additional check for bool.
        if not isinstance(duration, (int, float)) or isinstance(duration, bool):
            raise TypeError(f"value must be a number, got {type(duration)}")
        if duration < 0:
            raise ValueError(f"value must be >= 0, got {duration}")
        self._fade_duration = duration

    @property
    def brightness(self) -> float:
        """The display brightness in range 0-100.

        >>> backlight = Backlight()
        >>> backlight.brightness  # Display is at 50% brightness
        50
        >>> backlight.brightness = 100  # Set to full brightness

        :getter: Return the display brightness.
        :setter: Set the display brightness.
        :type: float
        """
        if self._board_type in (BoardType.RASPBERRY_PI, BoardType.MICROSOFT_SURFACE_RT):
            return self._normalize_brightness(self._get_value("actual_brightness"))
        elif (
            self._board_type == BoardType.TINKER_BOARD
            or self._board_type == BoardType.TINKER_BOARD_2
        ):
            return self._normalize_brightness(self._get_value("tinker_mcu_bl"))
        else:
            raise RuntimeError("Invalid board type")

    @brightness.setter
    def brightness(self, value: float) -> None:
        """Set the display brightness."""
        # isinstance(True, int) is True, so additional check for bool.
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"value must be a number, got {type(value)}")
        if value < 0 or value > 100:
            raise ValueError(f"value must be in range 0-100, got {value}")
        if self.fade_duration > 0:
            current_value = self.brightness
            step = 1 if current_value < value else -1
            diff = abs(value - current_value)
            while (
                0.0 <= current_value
                and current_value != value
                and current_value <= 100.0
            ):
                current_value += step
                if self._board_type in (
                    BoardType.RASPBERRY_PI,
                    BoardType.MICROSOFT_SURFACE_RT,
                ):
                    self._set_value(
                        "brightness", self._denormalize_brightness(current_value)
                    )
                elif (
                    self._board_type == BoardType.TINKER_BOARD
                    or self._board_type == BoardType.TINKER_BOARD_2
                ):
                    self._set_value(
                        "tinker_mcu_bl", self._denormalize_brightness(current_value)
                    )
                else:
                    raise RuntimeError("Invalid board type")
                time.sleep(self.fade_duration / diff)
        else:
            if self._board_type in (
                BoardType.RASPBERRY_PI,
                BoardType.MICROSOFT_SURFACE_RT,
            ):
                self._set_value("brightness", self._denormalize_brightness(value))
            elif (
                self._board_type == BoardType.TINKER_BOARD
                or self._board_type == BoardType.TINKER_BOARD_2
            ):
                self._set_value("tinker_mcu_bl", self._denormalize_brightness(value))
            else:
                raise RuntimeError("Invalid board type")

    @property
    def power(self) -> bool:
        """Turn the display on and off.

        >>> backlight = Backlight()
        >>> backlight.power  # Display is on
        True
        >>> backlight.power = False  # Turn display off

        :getter: Return whether the display is powered on or off.
        :setter: Set the display power on or off.
        :type: bool
        """
        if self._board_type in (BoardType.RASPBERRY_PI, BoardType.MICROSOFT_SURFACE_RT):
            # 0 is on, 1 is off
            return not self._get_value("bl_power")
        elif (
            self._board_type == BoardType.TINKER_BOARD
            or self._board_type == BoardType.TINKER_BOARD_2
        ):
            return bool(self._get_value("tinker_mcu_bl"))
        else:
            raise RuntimeError("Invalid board type")

    @power.setter
    def power(self, on: bool) -> None:
        """Set the display power on or off."""
        if not isinstance(on, bool):
            raise TypeError(f"value must be a bool, got {type(on)}")
        if self._board_type in (BoardType.RASPBERRY_PI, BoardType.MICROSOFT_SURFACE_RT):
            # 0 is on, 1 is off
            self._set_value("bl_power", int(not on))
        elif (
            self._board_type == BoardType.TINKER_BOARD
            or self._board_type == BoardType.TINKER_BOARD_2
        ):
            self._set_value("tinker_mcu_bl", 255 if on else 0)
        else:
            raise RuntimeError("Invalid board type")
