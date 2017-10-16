Changes
=======

1.8.1
-----

- Fix float division issue with Python 2

1.8.0
-----

- Fix permission error inconsistency across Python versions
- Update link to PyPI

1.7.1
-----

- Fixed typo in ``CHANGES.rst``
- Fixed rendering of parameters and return types in the documentation

1.7.0
-----

- Fixed bug in ``get_power``, which would eventually always return False
- Added parameters and return types in docstrings

1.6.0
-----

- Added ``duration`` parameter to ``set_brightness``
- ``smooth`` now defaults to ``False``
- Huge improvements on CLI
- Fixed renamed function in examples
- Minor code and readme improvements

1.5.0
-----

- PR #3 by Scouttp: Fixed permission errors
- Added documentation
- Code improvements
- Fixed typos

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
- Code improvements - thanks to deets

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
