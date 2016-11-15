Introduction
============

When I bought the official 7" touch LCD for my Raspberry Pi, I was happy about it. With one exception: *the display brightness*.

I googled some hours, and hacked somy Python code together. Time passed by, and the whole project turned into a Python module. rpi-backlight was born.

Maybe I should add some note here:

.. note::
   You may be confused about the different namings in the documentation:
   *rpi-backlight* and *rpi_backlight*. The first one is the project's name and
   also used for the GitHub repository. The second one is the Python module
   name, used on PyPI and when importing the module.

Currenly the code has the following features:

- Change the display brightness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness
- Get the display power state (on/off)
- Command line interface
- Graphical user interface

Now, you are able to easily set the brightness of your display from the commandline, a GUI and even Python code!

.. include:: global.rst
