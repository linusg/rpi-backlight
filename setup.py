from setuptools import setup
from rpi_backlight import __version__


with open("README.rst", "r") as f:
    long_description = f.read()

setup(name="rpi_backlight",
      py_modules=["rpi_backlight"],
      version=__version__,
      description="Python library containing some functions to control the 7\" touch display from the Raspberry Pi foundation.",
      long_description=long_description,
      author="Linus Groh",
      license="MIT",
      author_email="mail@linusgroh.de",
      url="https://github.com/linusg/rpi-backlight",
      download_url="https://pypi.python.org/pypi/rpi_backlight",
      keywords=["raspberry pi", "display", "touchscreen", "brightness"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Topic :: System :: Hardware",
          "Topic :: Multimedia",
          "Topic :: Utilities",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules"],
      )
