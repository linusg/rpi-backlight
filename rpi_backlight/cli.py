from argparse import ArgumentParser
from . import Backlight, __version__, BoardType


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
        choices=("on", "off"),
        help="set the display power (on/off)",
    )
    # parser.add_argument(
    #     "-s",
    #     "--smooth",
    #     action="store_true",
    #     help="sets a smooth fade",
    # )
    parser.add_argument(
        "-d", "--duration", type=float, default=0, help="fading duration in seconds"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        '-B', '--board', default=1,
        help='Please provide a board model.\n'
        '0: Raspberry Pi\n'
        '1: TinkerBoard\n.')
    return parser

def main():
    """Start the command line interface."""
    parser = _create_argument_parser()
    args = parser.parse_args()

    if args.board:
        board = int(args.board)
        if (board != 1 and board != 2):
            parser.error("Board parameter must be either 1 (Raspberry Pi) or 2 (TinkerBoard)")

    if (board == 2):
        if (args.sysfs_path is not None):
            backlight = Backlight(board_type=BoardType.TINKER_BOARD,backlight_sysfs_path=args.sysfs_path)
        elif (args.sysfs_path is None):
            backlight = Backlight(board_type=BoardType.TINKER_BOARD)
    elif (args.sysfs_path is not None):
            backlight = Backlight(backlight_sysfs_path=args.sysfs_path)
    else: 
        backlight = Backlight()


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
        if any(
            (args.get_brightness, args.set_brightness, args.get_power, args.duration)
        ):
            parser.error("-p/--set-power must be used without other options")
        backlight.power = True if args.set_power == "on" else False
        return

    if args.duration:
        parser.error("-d/--duration must be used with -b/--set-brightness")