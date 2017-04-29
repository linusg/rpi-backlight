Usage
=====

Application programming interface
---------------------------------

#. Make sure you've :ref:`installed <installation>` the library correctly.
#. Run Python as root (see the note at the end of this section) and import
   ``rpi_backlight``::

    >>> import rpi_backlight as bl

#. Now you can adjust the display power and brightness::

    >>> bl.set_brightness(255)
    >>> bl.set_brightness(20, smooth=True, duration=3)
    >>> bl.get_max_brightness()
    255
    >>> bl.get_actual_brightness()
    20
    >>> bl.get_power()
    True
    >>> bl.set_power(False)

   Also see the :ref:`rpi-backlight API` for reference.

   .. note::
      In order to run any of the ``set_`` functions, you have to edit the
      backlight permissions as described in the installation process or run
      your code as root, e.g. with ``sudo``.

Command line interface
----------------------

Open a terminal and run ``rpi-backlight`` as root, e.g.::

    $ rpi-backlight -b 255
    $ rpi-backlight -b 20 -s -d 3
    $ rpi-backlight --max-brightness
    255
    $ rpi-backlight --actual-brightness
    20
    $ rpi-backlight --power
    True
    $ rpi-backlight --off

Parameters::

    usage: rpi-backlight [-h] [-b VALUE] [-d DURATION] [-s] [--on] [--off]
                         [--max-brightness] [--actual-brightness] [--power]

    Control power and brightness of the official Raspberry Pi 7" touch display.

    optional arguments:
      -h, --help            show this help message and exit
      -b VALUE, --brightness VALUE
                            set the display brightness to VALUE (11-255)
      -d DURATION, --duration DURATION
                            fading duration in seconds
      -s, --smooth          fade the display brightness, see -d/--duration
      --on                  set the display powered on
      --off                 set the display powered off
      --max-brightness      get the maximum display brightness
      --actual-brightness   get the actual display brightness
      --power               get the current power state

Graphical user interface
------------------------

Open a terminal and run ``rpi-backlight-gui`` as root, e.g.::

    sudo rpi-backlight-gui

.. image:: https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/gui.png
   :alt: Graphical User Interface

.. include:: global.rst
