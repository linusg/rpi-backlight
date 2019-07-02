import sys

from . import Backlight


def main():
    """Start the graphical user interface."""
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk, GLib
    except ImportError:
        print("Please install pygobject to use the rpi-backlight GUI!")
        sys.exit()

    if len(sys.argv) > 1:
        backlight = Backlight(backlight_sysfs_path=sys.argv[1])
    else:
        backlight = Backlight()

    def update_scale():
        if scale.get_value() != backlight.brightness:
            scale.set_value(backlight.brightness)
        return True

    def update_brightness(*_):
        backlight.brightness = int(scale.get_value())

    window = Gtk.Window(title="rpi-backlight GUI")
    scale = Gtk.Scale(
        orientation=Gtk.Orientation.HORIZONTAL,
        adjustment=Gtk.Adjustment(
            value=backlight.brightness, lower=0, upper=100, step_increment=1
        ),
    )

    scale.connect("value-changed", update_brightness)
    scale.set_size_request(350, 50)

    main_container = Gtk.Fixed()
    main_container.put(scale, 10, 10)

    window.connect("delete-event", Gtk.main_quit)
    window.connect("destroy", Gtk.main_quit)
    window.add(main_container)
    window.resize(400, 50)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.show_all()

    GLib.timeout_add(100, update_scale)

    Gtk.main()
