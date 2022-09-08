from argparse import ArgumentParser

from . import Backlight, BoardType, __version__, utils

STRING_TO_BOARD_TYPE = {
    "raspberry-pi": BoardType.RASPBERRY_PI,
    "tinker-board": BoardType.TINKER_BOARD,
    "tinker-board-2": BoardType.TINKER_BOARD_2,
    "microsoft-surface-rt": BoardType.MICROSOFT_SURFACE_RT,
}

BOARD_TYPE_TO_STRING = {
    BoardType.RASPBERRY_PI: "raspberry-pi",
    BoardType.TINKER_BOARD: "tinker-board",
    BoardType.TINKER_BOARD_2: "tinker-board-2",
    BoardType.MICROSOFT_SURFACE_RT: "microsoft-surface-rt",
}


def _create_argument_parser():
    parser = ArgumentParser(
        description='Get/set power and brightness of the official Raspberry Pi 7" touch display.'
    )
    parser.add_argument(
        "sysfs_path",
        metavar="SYSFS_PATH",
        type=str,
        nargs="?",
        default=None,
        help="Optional path to the backlight sysfs, set to :emulator: to use with rpi-backlight-emulator",
    )
    parser.add_argument(
        "--get-brightness",
        action="store_true",
        help="get the display brightness (0-100)",
    )
    parser.add_argument(
        "-b",
        "--set-brightness",
        metavar="VALUE",
        type=int,
        choices=range(0, 101),
        help="set the display brightness (0-100)",
    )
    parser.add_argument(
        "--get-power", action="store_true", help="get the display power (on/off)"
    )
    parser.add_argument(
        "-p",
        "--set-power",
        metavar="VALUE",
        type=str,
        choices=("on", "off", "toggle"),
        help="set the display power (on/off/toggle)",
    )
    parser.add_argument(
        "-d", "--duration", type=float, default=0, help="fading duration in seconds"
    )
    parser.add_argument(
        "-B",
        "--board-type",
        default=BOARD_TYPE_TO_STRING.get(utils.detect_board_type(), "raspberry-pi"),
        choices=STRING_TO_BOARD_TYPE.keys(),
        help="board type",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main():
    """Start the command line interface."""
    parser = _create_argument_parser()
    args = parser.parse_args()

    backlight = Backlight(
        board_type=STRING_TO_BOARD_TYPE[args.board_type],
        backlight_sysfs_path=args.sysfs_path,
    )

    if args.get_brightness:
        if any((args.set_brightness, args.get_power, args.set_power, args.duration)):
            parser.error("--get-brightness must be used without other options")
        print(backlight.brightness)
        return

    if args.get_power:
        if any(
            (args.get_brightness, args.set_brightness, args.set_power, args.duration)
        ):
            parser.error("--get-power must be used without other options")
        print("on" if backlight.power else "off")
        return

    if args.set_brightness is not None:
        if any((args.get_brightness, args.get_power, args.set_power)):
            parser.error(
                "-b/--set-brightness must be used without other options except for -d/--duration"
            )
        # backlight.fade context manager can be used always as args.fade defaults to zero
        with backlight.fade(duration=args.duration):
            backlight.brightness = args.set_brightness
        return

    if args.set_power:
        if any((args.get_brightness, args.set_brightness, args.get_power)):
            parser.error("-p/--set-power may only be used with -d/--duration")
        if args.set_power == "toggle":
            if backlight.power:
                with backlight.fade(duration=args.duration):
                    backlight.brightness = 0
                if args.board_type == "raspberry-pi":
                    backlight.power = False
            else:
                # Ensure brightness is 0 when we turn the display on
                backlight.brightness = 0
                if args.board_type == "raspberry-pi":
                    backlight.power = True
                with backlight.fade(duration=args.duration):
                    backlight.brightness = 100
        else:
            backlight.power = True if args.set_power == "on" else False
        return

    if args.duration:
        parser.error(
            "-d/--duration must be used with -b/--set-brightness or -p/--set-power toggle"
        )
