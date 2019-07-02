# rpi-backlight

[![Travis CI](https://api.travis-ci.org/linusg/rpi-backlight.svg?branch=v2.0.0-alpha)](https://travis-ci.org/linusg/rpi-backlight)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](ttps://github.com/linusg/rpi-backlight/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/rpi-backlight.svg)](https://pypi.org/project/rpi-backlight/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://rpi-backlight.readthedocs.io/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/linusg/rpi-backlight.svg)](https://github.com/linusg/rpi-backlight/issues)

> A Python module for controlling power and brightness of the official Raspberry Pi 7" touch display.

![Example](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/example.gif)

**Note:** _This GIF was created using the old v1 API, so please don't use it as API reference 🙂_

## Features

- Change the display brightness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness
- Get the display power state (on/off)
- Command line interface
- Graphical user interface

## Requirements

- A **Raspberry Pi** including a correctly assembled **7" touch display v1.1 or higher**
  running a Linux-based OS
- Python 3.5+
- Optional: `pygobject` for the GUI, already installed on a recent Raspbian

## Installation

Install from PyPI:

```console
$ pip3 install rpi-backlight
```

**Note:** You may need to change the backlight rules file in order to run the code:

```console
$ echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
```

Otherwise you'll have to run Python code, The GUI and CLI as root when _changing_ the
power or brightness.

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

### CLI

Open a terminal and run `rpi-backlight`:

```console
$ rpi-backlight -b 100
$ rpi-backlight --set-brightness 20 --duration 1.5
$ rpi-backlight --get-brightness
20
$ rpi-backlight --get-power
on
$ rpi-backlight --p off
$ rpi-backlight --get-power
off
$ rpi-backlight --set-power off :emulator:
$
```

Available flags:

- `--get-brightness` - get brightness, will output value between 0 and 100
- `--get-power` - get power, will output `on` or `off`
- `-b` / `--set-brightness` - set brightness, provide value between 0 and 100
- `-p` / `--set-power` - set power on/off, provide `on` or `off`
- `-d` / `--duration` - use in combination with `-b` / `--brightness` to fade the
  brightness, provide value in seconds >= 0

You can set the backlight sysfs path using a positional argument, set it to `:emulator:`
to use with `rpi-backlight-emulator`.

### GUI

Open a terminal and run `rpi-backlight-gui`.

![Graphical User Interface](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/gui.png)
![Graphical User Interface (2)](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/gui2.png)

### Adding a shortcut to the LXDE panel

First, create a `.desktop` file for rpi-backlight (e.g.
`/home/pi/.local/share/applications/rpi-backlight.desktop`) with the following content:

```
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Name=rpi-backlight GUI
Exec=/home/pi/.local/bin/rpi-backlight-gui
Icon=/usr/share/icons/HighContrast/256x256/status/display-brightness.png
Categories=Utility;
```

_The absolute path to `rpi-backlight-gui` might differ if you did not follow the_
_installation instructions above, e.g. installed as root._

Make it executable:

```console
$ chmod +x /home/pi/.local/share/applications/rpi-backlight.desktop
```

You should now be able to start the rpi-backlight GUI from the menu:
`(Raspberry pi Logo) → Accessoires → rpi-backlight GUI`.

Next, right-click on the panel and choose `Add / Remove panel items`. Select
`Application Launch Bar` and click `Preferences`:

![Panel Preferences](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/panel_preferences.png)

Select `rpi-backlight GUI` on the right and click `Add`:

![Application Launch Bar](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/application_launch_bar.png)

You're done! The result should look like this:

![Panel Result](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/panel_result.png)

## Tests

Tests use `pytest`, install with `pip3 install pytest`.

Now, run from the repository root directory:

```console
$ python3 -m pytest
```

## Todo

I'm currently finalizing the 2.0.0 API and rebuilding the CLI - feel free to open an
issue for bug reports and to discuss new features!

## License

The source code and all other files in this repository are licensed under the MIT
license, so you can easily use it in your own projects. See [`LICENSE`](LICENSE) for
more information.
