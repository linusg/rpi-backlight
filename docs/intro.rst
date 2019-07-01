Introduction
============

.. image:: https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/example.gif
   :alt: Example

When I bought the official 7" touch LCD for my Raspberry Pi, I was happy
about it. With one exception: *you can't change the display brightness out of
the box*.

I did some research and hacked some Python code together. Time passed by,
and the whole project turned into a Python module: rpi-backlight.

Currently it has the following features:

- Change the display brightness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness
- Get the display power state (on/off)
- Command line interface
- Graphical user interface

Now you are able to easily set the brightness of your display from the
command line, a GUI and even Python code!

.. include:: global.rst
