"""
*A Python module for controlling power and brightness of the official Raspberry Pi 7" touch display.*

:Author: Linus Groh (mail@linusgroh.de)
:License: MIT license
"""
from __future__ import print_function
import time
import os
import sys

__author__ = "Linus Groh"
__version__ = "1.5.0"
PATH = "/sys/class/backlight/rpi_backlight/"


def _perm_denied():
    print("This program must be run as root!")
    sys.exit()


def _get_value(name):
    try:
        with open(os.path.join(PATH, name), "r") as f:
            return f.read()
    except PermissionError:
        _perm_denied()

def _set_value(name, value):
    with open(os.path.join(PATH, name), "w") as f:
        f.write(str(value))


def get_actual_brightness():
    """Return the actual display brightness."""
    return int(_get_value("actual_brightness"))


def get_max_brightness():
    """Return the maximum display brightness."""
    return int(_get_value("max_brightness"))


def get_power():
    """Return wether the display is powered on or not."""
    return not _get_value("bl_power")


def set_brightness(value, smooth=True):
    """Set the display brightness."""
    max_value = get_max_brightness()
    if type(value) != int:
        raise ValueError("integer required, got '{}'".format(type(value)))
    if not 10 < value <= max_value:
        raise ValueError("value must be between 11 and {}, got {}".format(max_value, value))
    
    if smooth:
        actual = get_actual_brightness()
        while actual != value:
            actual = actual - 1 if actual > value else actual + 1

            _set_value("brightness", actual)
            time.sleep(0.01)
    else:
        _set_value("brightness", value)


def set_power(on):
    """Set the display power on or off."""
    try:
        _set_value("bl_power", int(not on))
    except PermissionError:
        _perm_denied()


def cli():
    """Start the command line interface."""
    global input
    if sys.version.startswith("2"):
        input = raw_input
        
    while True:
        value = input("Enter value of brightness (between 11 and 255): ")
        try:
            value = int(value)
            if 10 < value < 256:
                break
            else:
                continue   
        except ValueError:
            continue
    set_brightness(value)


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
    
    def on_scale_changed(scale, _):
        value = int(scale.get_value())
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
