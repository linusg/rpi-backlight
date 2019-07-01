# rpi-backlight

[![Travis CI](https://api.travis-ci.org/linusg/rpi-backlight.svg?branch=v2.0.0-alpha)](https://travis-ci.org/linusg/rpi-backlight) [![Issues](https://img.shields.io/github/issues/linusg/rpi-backlight.svg)](https://github.com/linusg/rpi-backlight/issues) [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](ttps://github.com/linusg/rpi-backlight/blob/master/LICENSE) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![PyPI](https://img.shields.io/pypi/v/rpi_backlight.svg)](https://pypi.org/project/rpi_backlight/) [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://rpi-backlight.readthedocs.io/en/latest/)

> A Python module for controlling power and brightness of the official Raspberry Pi 7" touch display.

![Example](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/example.gif)

**Note:** _Since creation of this GIF, the API, specifically the default parameters of the `set_brightness` function, has changed a little bit, so please don't try to use it as the API reference 🙂_

## Features

- Change the display brightness **smoothly** or **abrupt**
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness
- Get the display power state (on/off)
- Command line interface
- Graphical user interface

## Requirements

- A **Raspberry Pi** including a correctly assembled **7" touch display v1.1 or higher** running a Linux-based OS
- Python 3.5+
- Optional: `pygobject` for the GUI, is likely to be already installed on a recent Raspbian

## Installation

Install from PyPI:

```console
$ pip3 install rpi_backlight
```

**Note:** You may need to change the backlight rules file in order to run the code:

```console
$ echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
```

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

**NOTE: Code using `set_` functions of this library has to be run as root, e.g. `sudo python3 file.py`, if the permissions for changing the backlight were not changed as described in the installation section!**

### CLI

Open a terminal and run `rpi-backlight`:

```console
$ rpi-backlight -b 255
$ rpi-backlight -b 20 -s -d 3
$ rpi-backlight --max-brightness
255
$ rpi-backlight --actual-brightness
20
$ rpi-backlight --power
True
$ rpi-backlight --off
```

### GUI

Open a terminal and run `rpi-backlight-gui`.

![Graphical User Interface](https://raw.githubusercontent.com/linusg/rpi-backlight/master/docs/gui.png)

### Adding a shortcut to the LXDE panel

First, create a `.desktop` file for rpi-backlight (e.g. `/home/pi/.local/share/applications/rpi-backlight.desktop`) with the following content:

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

_The absolute path to `rpi-backlight-gui` might differ if you did not follow the installation instructions above, e.g. installed as root._

Make it executable:

```console
$ chmod +x /home/pi/.local/share/applications/rpi-backlight.desktop
```

You should now be able to start the rpi-backlight GUI from the menu: `(Raspberry pi Logo) → Accessoires → rpi-backlight GUI`.

Next, right-click on the panel and choose `Add / Remove panel items`. Select `Application Launch Bar` and click `Preferences`:

![Panel Preferences](docs/panel_preferences.png)

Select `rpi-backlight GUI` on the right and click `Add`:

![Application Launch Bar](docs/application_launch_bar.png)

You're done! The result should look like this:

![Panel Result](docs/panel_result.png)

## Todo

Yay, this list is currently empty! Feel free to add ideas here.

## External Links

- [Travis CI: Build tests](https://travis-ci.org/linusg/rpi-backlight)
- [readthedocs.org: Documentation](https://rpi-backlight.readthedocs.io/en/latest/)

## License

The source code and all other files in this repository are licensed under the MIT license, so you can easily use it in your own projects. See [`LICENSE`](LICENSE) for more information.
