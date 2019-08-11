.. _installation:

Installation
============

This section covers the installation of the library on the Raspberry Pi.

Requirements
------------

- A **Raspberry Pi** including a correctly assembled **7" touch display v1.1 or higher**
  (look on the display's circuit board to see its version) running a Linux-based OS.
  Alternatively you can use rpi-backlight-emulator_ on all operating systems and without
  the actual hardware.
- Python 3.5+
- Optional: ``pygobject`` for the GUI, already installed on a recent Raspbian

Installation
------------

.. note::
   This library will **not** work with Windows IoT, you'll need a Linux distribution
   running on your Raspberry Pi. This was tested with Raspbian 9 (Stretch) and 10 (Buster).

rpi-backlight is available on PyPI_, so you can install it using ``pip3``:

.. code-block:: console

    $ pip3 install rpi_backlight

**Note:** Create this udev rule to update permissions, otherwise you'll have to run
Python code, the GUI and CLI as root when *changing* the power or brightness:

.. code-block:: console

    $ echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

rpi-backlight is now installed. See :ref:`Usage <usage>` to get started!

.. include:: global.rst
