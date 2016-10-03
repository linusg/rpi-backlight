"""rpi_backlight.py
A Python module for controlling power and brightness of the official Raspberry Pi 7" touch display.
"""
from __future__ import print_function
import time
import os
import sys

__author__ = "Linus Groh"
__version__ = "1.1.0"
PATH = "/sys/class/backlight/rpi_backlight/"


def _perm_denied():
    print("This program must be run as root!")
    sys.exit()


def _get_value(name):
    with open(os.path.join(PATH, name), "r") as f:
        return int(f.read())


def _set_value(name, value):
    with open(os.path.join(PATH, name), "w") as f:
        f.write(value)


def get_actual_brightness():
    """Return the actual display brightness."""
    return _get_value("actual_brightness")


def get_max_brightness():
    """Return the maximum display brightness."""
    return _get_value("max_brightness")


def get_power():
    """Return wether the display is powered on or not."""
    try:
        return not _get_value("bl_power")
    except PermissionError:
        _perm_denied()


def set_brightness(value, smooth=True):
    """Set the display brightness."""
    if not 10 < value <= get_max_brightness() or type(value) != int:
        raise ValueError("value must be between 11 and {}, got {}".format(max_value, value))

    def run(value):
        try:
            _set_value("brightness", str(value))
        except PermissionError:
            _perm_denied()
    
    if smooth:
        actual = get_actual_brightness()
        while actual != value:
            actual = actual - 1 if actual > value else actual + 1

            run(actual)
            time.sleep(0.01)
    else:
        run(value)


def set_power(on):
    """Power the display power on or off."""
    try:
        if on:
            _set_value("bl_power", "0")
        else:
            _set_value("bl_power", "1")
    except PermissionError:
        _perm_denied()


if __name__ == "__main__":
    if sys.version.startswith("2"):
        input = raw_input
        
    success = False
    while not success:
        value = input("Enter value of brightness (between 11 and 255): ")
        try:
            value = int(value)
        except ValueError:
            continue
        if 10 < value < 256:
            set_brightness(value)
            success = True
