# rpi-backlight

> A Python module for controlling power and brightness of the official Raspberry Pi 7" touch display.

[![PyPI](https://img.shields.io/pypi/v/rpi-backlight)](https://pypi.org/project/rpi-backlight/)
![Python Version](https://img.shields.io/pypi/pyversions/rpi-backlight)
[![Downloads](https://pepy.tech/badge/rpi-backlight)](https://pepy.tech/project/rpi-backlight)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://rpi-backlight.readthedocs.io/en/latest/)
[![License](https://img.shields.io/github/license/linusg/rpi-backlight?color=d63e97)](https://github.com/linusg/rpi-backlight/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/ambv/black)
[![Build](https://github.com/linusg/rpi-backlight/workflows/Build/badge.svg)](https://github.com/linusg/rpi-backlight/actions?query=workflow%3ABuild)
[![Read the Docs](https://img.shields.io/readthedocs/rpi-backlight)](https://rpi-backlight.readthedocs.io/en/latest/)
[![Issues](https://img.shields.io/github/issues/linusg/rpi-backlight)](https://github.com/linusg/rpi-backlight/issues)

![Example](https://raw.githubusercontent.com/linusg/rpi-backlight/main/docs/_static/example.gif)

**Note:** _This GIF was created using the old v1 API, so please don't use it as API reference 🙂_

## Features

- Set the display brightness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the display power state (on/off)
- Command line interface
- Graphical user interface

## Requirements

- A **Raspberry Pi or ASUS Tinker Board** including a correctly assembled **7" touch display v1.1 or higher**
  (look on the display's circuit board to see its version), or a [**Surface RT**](https://openrt.gitbook.io/open-surfacert/surface-rt/linux/root-filesystem/distros/raspberry-pi-os) running a Linux-based OS
- Python 3.6+
- Optional: Raspberry Pi: ``pygobject`` for the GUI, already installed on a recent Raspbian
- Optional: Tinker Board: ``gir1.2-gtk-3.0`` for the GUI install

## Installation

Install from PyPI:

```console
$ pip3 install rpi-backlight
```

**Note:** Create this udev rule to update permissions, otherwise you'll have to run
Python code, the GUI and CLI as root when _changing_ the power or brightness:

```console
$ echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
```

### Emulator

For testing without a physical display (e.g. on your main Linux/macOS/Windows machine)
you can use [`linusg/rpi-backlight-emulator`](https://github.com/linusg/rpi-backlight-emulator).

## Usage

### API

Example in a Python shell:

```python
>>> from rpi_backlight import Backlight
>>>
>>> backlight = Backlight()
>>> backlight.brightness
100
>>> backlight.brightness = 50
>>> backlight.brightness
50
>>>
>>> with backlight.fade(duration=1):
...     backlight.brightness = 0
...
>>> backlight.fade_duration = 0.5
>>> # subsequent `backlight.brightness = x` will fade 500ms
>>>
>>> backlight.power
True
>>> backlight.power = False
>>> backlight.power
False
>>>
```

For more details see [docs](https://rpi-backlight.readthedocs.io/en/latest/api.html).

### CLI

Open a terminal and run `rpi-backlight`.

```console
$ rpi-backlight -b 100
$ rpi-backlight --set-brightness 20 --duration 1.5
$ rpi-backlight --get-brightness
20
$ rpi-backlight --get-power
on
$ rpi-backlight -p off
$ rpi-backlight --get-power
off
$ rpi-backlight --set-power off :emulator:
$ rpi-backlight -p toggle
$ rpi-backlight -p toggle -d 1.5
$
```

For all available options see [docs](https://rpi-backlight.readthedocs.io/en/latest/usage.html#command-line-interface).

### GUI

Open a terminal and run `rpi-backlight-gui`.

![Graphical User Interface](https://raw.githubusercontent.com/linusg/rpi-backlight/main/docs/_static/gui.png)
![Graphical User Interface (2)](https://raw.githubusercontent.com/linusg/rpi-backlight/main/docs/_static/gui2.png)

### Adding a shortcut to the LXDE panel

![Panel result](https://raw.githubusercontent.com/linusg/rpi-backlight/main/docs/_static/panel_result.png)

See [docs](https://rpi-backlight.readthedocs.io/en/latest/usage.html#adding-a-shortcut-to-the-lxde-panel).

## Tests

Tests use `pytest`, install with `pip3 install pytest`.

Now, run from the repository root directory:

```console
$ python3 -m pytest
```

## Contributing

Please free to open an issue for bug reports and to discuss new features - pull requests for new features or bug fixes are welcome as well!

## License

The source code and all other files in this repository are licensed under the MIT
license, so you can easily use it in your own projects. See [`LICENSE`](LICENSE) for
more information.
