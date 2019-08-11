import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Callable, Union

__author__ = "Linus Groh"
__version__ = "2.0.0"
__all__ = ["Backlight"]

_BACKLIGHT_SYSFS_PATH = "/sys/class/backlight/rpi_backlight/"
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
        self, backlight_sysfs_path: Union[str, bytes, Path] = _BACKLIGHT_SYSFS_PATH
    ):
        """Set ``backlight_sysfs_path`` to ``":emulator:"`` to use with rpi-backlight-emulator."""
        if backlight_sysfs_path == _EMULATOR_MAGIC_STRING:
            if not _EMULATOR_SYSFS_TMP_FILE_PATH.exists():
                raise RuntimeError(
                    "Emulator seems to be not running, {0} not found".format(
                        _EMULATOR_SYSFS_TMP_FILE_PATH
                    )
                )
            backlight_sysfs_path = _EMULATOR_SYSFS_TMP_FILE_PATH.read_text()
        self._backlight_sysfs_path = Path(backlight_sysfs_path)
        self._max_brightness = self._get_value("max_brightness")  # 255
        self._fade_duration = 0  # in seconds

    def _get_value(self, name: str) -> int:
        try:
            return int((self._backlight_sysfs_path / name).read_text())
        except ValueError:
            # Reading failed, sometimes file is empty when updating
            # Try again
            return self._get_value(name)
        except (OSError, IOError) as e:
            if e.errno == 13:
                _permission_denied()
            raise e

    def _set_value(self, name: str, value: int) -> None:
        try:
            (self._backlight_sysfs_path / name).write_text(str(value))
        except (OSError, IOError) as e:
            if e.errno == 13:
                _permission_denied()
            raise e

    def _normalize_brightness(self, value: int) -> int:
        return int(round(value / self._max_brightness * 100))

    def _denormalize_brightness(self, value: int) -> int:
        return int(round(value * self._max_brightness / 100))

    @contextmanager
    def fade(self, duration: float) -> None:
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
            raise TypeError("value must be a number, got {0}".format(type(duration)))
        if duration < 0:
            raise ValueError("value must be >= 0, got {0}".format(duration))
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
        return self._normalize_brightness(self._get_value("actual_brightness"))

    @brightness.setter
    def brightness(self, value: float) -> None:
        """Set the display brightness."""
        # isinstance(True, int) is True, so additional check for bool.
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("value must be a number, got {0}".format(type(value)))
        if value < 0 or value > 100:
            raise ValueError("value must be in range 0-100, got {0}".format(value))

        if self.fade_duration > 0:
            current_value = self.brightness
            step = 1 if current_value < value else -1
            diff = abs(value - current_value)
            while current_value != value:
                current_value += step
                self._set_value(
                    "brightness", self._denormalize_brightness(current_value)
                )
                time.sleep(self.fade_duration / diff)
        else:
            self._set_value("brightness", self._denormalize_brightness(value))

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
        # 0 is on, 1 is off
        return not self._get_value("bl_power")

    @power.setter
    def power(self, on: bool) -> bool:
        """Set the display power on or off."""
        if not isinstance(on, bool):
            raise TypeError("value must be a bool, got {0}".format(type(on)))
        # 0 is on, 1 is off
        self._set_value("bl_power", int(not on))
