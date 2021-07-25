from pathlib import Path

import pytest

from rpi_backlight import BoardType
from rpi_backlight.utils import FakeBacklightSysfs, detect_board_type


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


@pytest.mark.parametrize(
    "model,board_type",
    [
        ("Raspberry Pi 3 Model B Rev 1.2", BoardType.RASPBERRY_PI),
        ("Raspberry Pi 42", BoardType.RASPBERRY_PI),
        ("Raspberry Pi", BoardType.RASPBERRY_PI),
        ("ASUS Tinker Board 2", BoardType.TINKER_BOARD_2),
        ("ASUS Tinker Board 2S", BoardType.TINKER_BOARD_2),
        ("Tinker Board 2", BoardType.TINKER_BOARD_2),
        ("Tinker Board 2S", BoardType.TINKER_BOARD_2),
        ("Rockchip RK3288 Asus Tinker Board", BoardType.TINKER_BOARD),
        ("Rockchip RK3288 Asus Tinker Board S", BoardType.TINKER_BOARD),
        ("Tinker Board", BoardType.TINKER_BOARD),
        ("Something else", None),
    ],
)
def test_detect_board_type(monkeypatch, model, board_type) -> None:
    monkeypatch.setattr(Path, "read_text", lambda self: model)

    assert detect_board_type() == board_type
