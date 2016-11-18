.. _installation:

Installation
============

This section covers the installation of the library on the Raspberry Pi.

Requirements
------------

- A **Raspberry Pi** (obviously) including a correctly assembled **7" touch
  display v1.1 or higher**. There's no way to get the version programmatically,
  just look on the display's circuit board.
- Python 2 or 3
- Optional: ``pygobject`` for the GUI, is likely to be already installed on a
  recent Raspbian

Installation process
--------------------

.. warning::
   This library will **not** work with Windows IoT, you'll need a Linux
   distribution running on your Raspi. This was tested with Raspbian.

#. Open up a terminal.

#. The rpi-backlight library is available on PyPI_, so you can install it
   using ``pip``::

    pip install rpi_backlight

   As an alternative you can get the source code from GitHub_ and install it
   using the setup script::

    sudo python setup.py install
    
    
  **Note:** You may need to edit the backlight rules file in order to run the code::

    sudo nano /etc/udev/rules.d/backlight-permissions.rules

  Insert the line::

    SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"

#. Just check the installation::

    >>> import rpi_backlight
    >>> 

   And here we go!

.. include:: global.rst
