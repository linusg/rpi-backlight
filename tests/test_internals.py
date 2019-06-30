import pytest
from rpi_backlight import Backlight, _permission_denied
from rpi_backlight.utils import FakeBacklightSysfs


def test_permission_denied() -> None:
    with pytest.raises(PermissionError):
        _permission_denied()


def test_get_value() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight._get_value("brightness") == 255


def test_set_value() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight._set_value("brightness", 0) is None
        assert backlight._get_value("brightness") == 0


def test_normalize_brightness() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight._normalize_brightness(255) == 100
        assert backlight._normalize_brightness(128) == 50
        assert backlight._normalize_brightness(0) == 0


def test_denormalize_brightness() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight._denormalize_brightness(100) == 255
        assert backlight._denormalize_brightness(50) == 128
        assert backlight._denormalize_brightness(0) == 0
