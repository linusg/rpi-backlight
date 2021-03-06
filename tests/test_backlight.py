import pytest

from rpi_backlight import Backlight, _EMULATOR_SYSFS_TMP_FILE_PATH
from rpi_backlight.utils import FakeBacklightSysfs


def test_constructor() -> None:
    with pytest.raises(TypeError):
        Backlight(board_type="foo")  # type: ignore[arg-type]

    assert not _EMULATOR_SYSFS_TMP_FILE_PATH.exists()
    with pytest.raises(RuntimeError):
        Backlight(backlight_sysfs_path=":emulator:")


def test_get_fade_duration() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight.fade_duration == 0


def test_set_fade_duration() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        backlight.fade_duration = 0.5
        assert backlight.fade_duration == 0.5

        backlight.fade_duration = 1
        assert backlight.fade_duration == 1

        with pytest.raises(ValueError):
            backlight.fade_duration = -1

        with pytest.raises(TypeError):
            backlight.fade_duration = "foo"  # type: ignore[assignment]

        with pytest.raises(TypeError):
            backlight.fade_duration = True


def test_get_brightness() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight.brightness == 100


def test_set_brightness() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        backlight.brightness = 50
        assert backlight.brightness == 50

        backlight.brightness = 0
        assert backlight.brightness == 0

        with pytest.raises(TypeError):
            backlight.brightness = "foo"  # type: ignore[assignment]

        with pytest.raises(TypeError):
            backlight.brightness = True

        with pytest.raises(ValueError):
            backlight.brightness = 101

        with pytest.raises(ValueError):
            backlight.brightness = -1


def test_get_power() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight.power is True


def test_set_power() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        backlight.power = False
        assert backlight.power is False

        backlight.power = True
        assert backlight.power is True

        with pytest.raises(TypeError):
            backlight.power = "foo"  # type: ignore[assignment]

        with pytest.raises(TypeError):
            backlight.power = 1  # type: ignore[assignment]


def test_fade() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        backlight = Backlight(backlight_sysfs_path=backlight_sysfs.path)

        assert backlight.fade_duration == 0

        backlight.fade_duration = 0.1
        assert backlight.fade_duration == 0.1

        with backlight.fade(duration=0.5) as _val:
            assert _val is None
            assert backlight.fade_duration == 0.5

        assert backlight.fade_duration == 0.1
