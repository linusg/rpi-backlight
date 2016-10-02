import time
import os
import sys

__author__ = "Linus Groh"
__version__ = "1.0.0"
path = "/sys/class/backlight/rpi_backlight/"


def _perm_denied():
    print("This program must be run as root!")
    sys.exit()


def get_actual_brightness():
    global path
    with open(os.path.join(path, "actual_brightness"), "r") as f:
        return int(f.read())


def get_max_brightness():
    global path
    with open(os.path.join(path, "max_brightness"), "r") as f:
        return int(f.read())


def set_brightness(value, smooth=True):
    global path
    if not 10 < value <= get_max_brightness() or type(value) != int:
        raise ValueError("value must be between 11 and {}, got {}".format(max_value, value))

    def run(value):
        try:
            with open(os.path.join(path, "brightness"), "w") as f:
                f.write(str(value))
        except PermissionError:
            _perm_denied()
    
    if smooth:
        v = get_actual_brightness()
        while v != value:
            v = v - 1 if v > value else v + 1

            run(v)
            time.sleep(0.01)
    else:
        run(value)


def set_power(on):
    try:
        with open(os.path.join(path, "bl_power"), "w") as f:
            if on:
                f.write("0")
            else:
                f.write("1")
    except PermissionError:
        _perm_denied()


if __name__ == "__main__":
    if sys.version.startswith("2"):
        input = raw_input
        
    success = False
    while not success:
        v = input("Enter value of brightness (between 11 and 255): ")
        try:
            v = int(v)
        except ValueError:
            continue
        if 10 < v < 256:
            set_brightness(v)
            success = True
