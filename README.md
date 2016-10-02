# rpi-backlight
## Python library containing some functions to control the 7" touch display from the Raspberry Pi foundation.

**WARNING: This comes with absolutely no warranty, do anything on your own risk!**

The code is very small and simple, but will be extended in the future for new features. Feel free to contribute!

## Features:
- Change the display brigntness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness

## Example

    >>> import rpi_backlight as bl
    >>> bl.set_brightness(20, smooth=True)
    >>> bl.set_brightness(255, smooth=True)
    >>> bl.set_brightness(20, smooth=False)
    >>> bl.max_brightness
    255
    >>> bl.current_brightness
    20
    >>> bl.set_power(False)

**NOTE: Code using this library has to be run as root, e.g. `sudo python file.py`!**

## Todo
- Create a really simple GUI in `pygobject` to change the display brightness, maybe just a scale/slider

I would be happy if you can help shortening this todo-list!

## License
The source code and all other files in this repository are licensed under the MIT license, so you can easily use it in your own projects.
