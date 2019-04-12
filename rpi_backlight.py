"""
A Python module for controlling power and brightness
of the official Raspberry Pi 7" touch display.

Ships with a CLI, GUI and Python API.

:Author: Linus Groh
:License: MIT license
"""

import argparse
import os
import sys
import time
from typing import Any

__author__ = "Linus Groh"
__version__ = "1.8.1"
PATH = "/sys/class/backlight/rpi_backlight/"
MODE_TINKERBOARD = "TINKERBOARD"
MODE_RPI = "RPI"
MODE = MODE_RPI

def _perm_denied() -> None:
    print(
        "A permission error occured. You must either run this program as root or change the"
    )
    print("permissions for the backlight access as described on the GitHub page.")
    sys.exit()


def _get_value(name: str) -> str:
    try:
        with open(os.path.join(PATH, name), "r") as f:
            return f.read()
    except (OSError, IOError) as err:
        if err.errno == 13:
            _perm_denied()


def _set_value(name: str, value: Any) -> None:
    try:
        with open(os.path.join(PATH, name), "w") as f:
            f.write(str(value))
    except (OSError, IOError) as err:
        if err.errno == 13:
            _perm_denied()


def _set_brightness_value(value: int) -> None:
    if MODE == MODE_TINKERBOARD:
        _set_value("tinker_mcu_bl", value)
    elif MODE == MODE_RPI:
        _set_value("bl_power", value)

def get_actual_brightness() -> int:
    """Return the actual display brightness."""
    if MODE == MODE_TINKERBOARD:
        return int(_get_value("tinker_mcu_bl"))
    elif MODE == MODE_RPI:
        return int(_get_value("actual_brightness"))

def get_max_brightness() -> int:
    """Return the maximum display brightness."""
    if MODE == MODE_TINKERBOARD:
        return 255
    elif MODE == MODE_RPI:
        return int(_get_value("max_brightness"))
    

def get_power() -> bool:
    """Return whether the display is powered on or not."""
    # 0 is on, 1 is off
    if MODE == MODE_TINKERBOARD:
        if get_actual_brightness():
            return True
        else:
            return False
    elif MODE == MODE_RPI:
        return not int(_get_value("bl_power"))


def set_brightness(value: int, smooth: bool = False, duration: float = 1) -> None:
    """Set the display brightness.

    :param value: Brightness value between 0 and 255
    :param smooth: Boolean if the brightness should be faded or not
    :param duration: Fading duration in seconds
    """
    max_value = get_max_brightness()
    if not isinstance(value, int):
        raise ValueError("integer required, got '{}'".format(type(value)))
    if not -1 < value <= max_value:
        raise ValueError(
            "value must be between 0 and {}, got {}".format(max_value, value)
        )
    if smooth:
        if not isinstance(duration, (int, float)):
            raise ValueError(
                "integer or float required, got '{}'".format(type(duration))
            )
        actual = get_actual_brightness()
        diff = abs(value - actual)
        while actual != value:
            actual = actual - 1 if actual > value else actual + 1
            _set_brightness_value(actual)
            time.sleep(duration / diff)
    else:
        _set_brightness_value(value)


def set_power(on: bool) -> None:
    """Set the display power on or off.
    :param on: Boolean whether the display should be powered on or not
    """
    # 0 is on, 1 is off
    if MODE == MODE_RPI:
        _set_value("bl_power", int(not get_power))
    elif MODE == MODE_TINKERBOARD:
        if on:
            value = 255
        else: 
            value = 0
        _set_brightness_value(value)


def toggle_power() -> None:
    """Toggle the display power on or off."""
    set_power(not get_power())

def _create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Control power and brightness of the "
        'official Raspberry Pi 7" touch display.'
    )

    parser.add_argument(
        "-b",
        "--brightness",
        metavar="VALUE",
        type=int,
        choices=range(256),
        help="set the display brightness to VALUE (0-255)",
    )

    parser.add_argument(
        "-d", "--duration", type=int, default=1, help="fading duration in seconds"
    )
    parser.add_argument(
        "-s",
        action="store_true",
        help="fade the display brightness, see -d/--duration",
    )
    parser.add_argument("--on", action="store_true", help="set the display powered on")
    parser.add_argument(
        "--off", action="store_true", help="set the display powered off"
    )
    parser.add_argument(
        "--toggle",
        action="store_true",
        help="toggle the display power",
    )
    
    parser.add_argument(
        "--max-brightness",
        action="store_true",
        help="get the maximum display brightness",
    )
    parser.add_argument(
        "--actual-brightness",
        action="store_true",
        help="get the actual display brightness",
    )
    parser.add_argument(
        "--power", action="store_true", help="get the current power state"
    )
    return parser

def init() -> None:
    global MODE, PATH
    try:
        with open("/sys/firmware/devicetree/base/model") as f:
            model_information = f.read()
        if "Raspberry Pi" in model_information:
            PATH = "/sys/class/backlight/rpi_backlight/"
            MODE = MODE_RPI
        elif "Tinker Board" in model_information:
            PATH = "/sys/devices/platform/ff150000.i2c/i2c-3/3-0045/"
            MODE = MODE_TINKERBOARD
    except Exception as error:
        raise Exception("unsupported OS, or OS could not be detected!")

def cli() -> None:
    """Start the command line interface."""
    init()
    parser = _create_argument_parser()
    args = parser.parse_args()

    if all(
        arg in (False, None)
        for arg in (
            args.off,
            args.on,
            args.toggle,
            args.brightness,
            args.max_brightness,
            args.actual_brightness,
            args.power,
            args.duration, 
        )
    ):
        parser.print_help()

    if args.off:
        set_power(False)

    if args.on:
        set_power(True)

    if isinstance(args.brightness, int):
        set_brightness(args.brightness, args.smooth, args.duration)

    if args.max_brightness:
        print(get_max_brightness())

    if args.actual_brightness:
        print(get_actual_brightness())

    if args.power:
        print(get_power())
        
    if args.toggle:
        toggle_power()


def gui() -> None:
    """Start the graphical user interface."""
    init()
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
    except ImportError:
        print("Sorry, this needs pygobject to be installed!")
        sys.exit()

    win = Gtk.Window(title="Set display brightness")
    ad1 = Gtk.Adjustment(value=get_actual_brightness(), lower=0, upper=255)
    scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)

    def on_scale_changed(s, _):
        value = int(s.get_value())
        set_brightness(value)

    scale.connect("button-release-event", on_scale_changed)
    scale.connect("key_release_event", on_scale_changed)
    scale.connect("scroll-event", on_scale_changed)
    scale.set_size_request(350, 50)

    # Main Container
    main_container = Gtk.Fixed()
    main_container.put(scale, 10, 10)

    # Main Window
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.add(main_container)
    win.resize(400, 50)
    win.set_position(Gtk.WindowPosition.CENTER)

    win.show_all()
    Gtk.main()
