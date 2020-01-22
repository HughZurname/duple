from duple.service import run
from duple.console import console_deduplicate
from optparse import OptionParser


def parse_options():
    parser = OptionParser(usage="stressjr [options]")

    parser.add_option(
        "-s",
        "--service",
        action="store_const",
        const="service",
        dest="command",
        help="Run duple in service mode.",
    )

    parser.add_option(
        "-c",
        "--console",
        action="store_const",
        const="console",
        dest="command",
        help="Run duple in console mode along with the -f command to supply a file",
    )

    parser.add_option(
        "-f",
        "--file",
        action="store",
        type="string",
        dest="filename",
        help="Supply a csv file to deduplicate",
    )

    opts, args = parser.parse_args()

    return parser, opts, args


(parser, options, args) = parse_options()

if options.command == "service":
    run()
elif options.command == "console":
    if not options.filename:
        parser.error("No file supplied with -c command")
    else:
        console_deduplicate(options.filename)
