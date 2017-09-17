"""
A Python module for controlling power and brightness
of the official Raspberry Pi 7" touch display.

Ships with a CLI, GUI and Python API.

:Author: Linus Groh
:License: MIT license
"""
from __future__ import print_function
import time
import os
import sys
import argparse

__author__ = "Linus Groh"
__version__ = "1.8.0"
PATH = "/sys/class/backlight/rpi_backlight/"


def _perm_denied():
    print("A permission error occured. You must either run this program as root or change the")
    print("permissions for the backlight access as described on the GitHub page.")
    sys.exit()


def _get_value(name):
    try:
        with open(os.path.join(PATH, name), "r") as f:
            return f.read()
    except (OSError, IOError) as err:
        if err.errno == 13:
            _perm_denied()


def _set_value(name, value):
    try:
        with open(os.path.join(PATH, name), "w") as f:
            f.write(str(value))
    except (OSError, IOError) as err:
        if err.errno == 13:
            _perm_denied()


def get_actual_brightness():
    """Return the actual display brightness.

    :return: Actual brightness value.
    :rtype: int
    """

    return int(_get_value("actual_brightness"))


def get_max_brightness():
    """Return the maximum display brightness.

    :return: Maximum possible brightness value.
    :rtype: int
    """

    return int(_get_value("max_brightness"))


def get_power():
    """Return wether the display is powered on or not.

    :return: Whether the diplay is powered on or not.
    :rtype: bool
    """

    return not int(_get_value("bl_power"))


def set_brightness(value, smooth=False, duration=1):
    """Set the display brightness.

    :param value: Brightness value between 11 and 255
    :param smooth: Boolean if the brightness should be faded or not
    :param duration: Fading duration in seconds
    """

    max_value = get_max_brightness()
    if not isinstance(value, int):
        raise ValueError(
            "integer required, got '{}'".format(type(value)))
    if not 10 < value <= max_value:
        raise ValueError(
            "value must be between 11 and {}, got {}".format(max_value, value))

    if smooth:
        if not isinstance(duration, (int, float)):
            raise ValueError(
                "integer or float required, got '{}'".format(type(duration)))
        actual = get_actual_brightness()
        diff = abs(value-actual)
        while actual != value:
            actual = actual - 1 if actual > value else actual + 1

            _set_value("brightness", actual)
            time.sleep(duration/diff)
    else:
        _set_value("brightness", value)


def set_power(on):
    """Set the display power on or off.

    :param on: Boolean whether the display should be powered on or not
    """

    _set_value("bl_power", int(not on))


def cli():
    """Start the command line interface."""
    parser = argparse.ArgumentParser(
        description="Control power and brightness of the "
                    "official Raspberry Pi 7\" touch display.")
    parser.add_argument("-b", "--brightness", metavar='VALUE',
                        type=int, choices=range(11, 256),
                        help="set the display brightness to VALUE (11-255)")
    parser.add_argument("-d", "--duration", type=int, default=1,
                        help="fading duration in seconds")
    parser.add_argument("-s", "--smooth", action='store_true',
                        help="fade the display brightness, see -d/--duration")
    parser.add_argument("--on", action='store_true',
                        help="set the display powered on")
    parser.add_argument("--off", action='store_true',
                        help="set the display powered off")
    parser.add_argument("--max-brightness", action='store_true',
                        help="get the maximum display brightness")
    parser.add_argument("--actual-brightness", action='store_true',
                        help="get the actual display brightness")
    parser.add_argument("--power", action='store_true',
                        help="get the current power state")
    args = parser.parse_args()

    if all(arg in (False, None) for arg in (
            args.off, args.on, args.brightness, args.max_brightness,
            args.actual_brightness, args.power)):
        parser.print_help()

    if args.off is True:
        set_power(False)

    if args.on is True:
        set_power(True)

    if args.brightness:
        set_brightness(args.brightness, args.smooth, args.duration)

    if args.max_brightness:
        print(get_max_brightness())

    if args.actual_brightness:
        print(get_actual_brightness())

    if args.power:
        print(get_power())


def gui():
    """Start the graphical user interface."""
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
    except ImportError:
        print("Sorry, this needs pygobject to be installed!")
        sys.exit()

    win = Gtk.Window(title="Set display brightness")

    ad1 = Gtk.Adjustment(value=get_actual_brightness(), lower=11, upper=255)
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
