from rpi_backlight.utils import FakeBacklightSysfs


def test_fake_sysfs_backlight() -> None:
    with FakeBacklightSysfs() as backlight_sysfs:
        assert backlight_sysfs.path.exists() is True
        for filename in (
            "bl_power",
            "brightness",
            "actual_brightness",
            "max_brightness",
        ):
            assert (backlight_sysfs.path / filename).exists() is True

    assert backlight_sysfs.path.exists() is False
