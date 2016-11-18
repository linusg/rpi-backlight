Changes
=======

1.5.0
-----

- PR #3 by Scouttp: Fixed permission errors

1.4.0
-----

- Check for ``pygobject`` being installed
- Code cleanup
- README improvements

  - Added external links
  - Added badges
  - Fixed typos

- Moved to Travis CI and Landscape.io for builds and code health testing
- Prepared docs hosting at readthedocs.org

1.3.1
-----

- Fixed type conversion

1.3.0
-----

- Added experimental GUI (start with ``rpi-backlight-gui``)

1.2.1
-----

- Fixed CLI and typo

1.2.0
-----

- Added command line interface (`rpi-backlight` and `rpi-backlight-gui`)
- Code improvements - thanks @deets

1.1.0
-----

- Fixed ``set_power(on)`` function
- Added function to get the current power state of the LCD
- Added docstrings
- Code cleanup and improvements

1.0.0
-----

Initial release. Added necessary files and basic features:

- Change the display brightness smoothly or abrupt
- Set the display power on or off
- Get the current brightness
- Get the maximum brightness
