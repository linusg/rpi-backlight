Usage
=====

Application programming interface
---------------------------------

#. Make sure you've :ref:`installed <installation>` the library correctly.
#. Run Python as root (see the note at the end of this section) and import
   ``rpi_backlight``::

    >>> import rpi_backlight as bl

#. Now you can adjust the display power and brightness::

    >>> bl.set_brightness(20)
    >>> bl.set_brightness(255)
    >>> bl.set_brightness(20, smooth=False)
    >>> bl.get_max_brightness()
    255
    >>> bl.get_current_brightness()
    20
    >>> bl.get_power()
    True
    >>> bl.set_power(False)

   Also see the :ref:`rpi-backlight API` for reference.

   .. note::
      In order to run any of the ``set_`` functions, you have to run your
      code as root, e.g. with ``sudo``.

Command line interface
----------------------

Open a terminal and run ``rpi-backlight`` as root, e.g.::

    sudo rpi-backlight

.. image:: https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/cli.png
   :alt: Command Line Interface

Graphical user interface
------------------------

Open a terminal and run ``rpi-backlight-gui`` as root, e.g.::

    sudo rpi-backlight-gui

.. image:: https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/gui.png
   :alt: Graphical User Interface

.. include:: global.rst
