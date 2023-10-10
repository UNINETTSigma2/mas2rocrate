import argparse
import json
import sys

from .config import get_config, Config
from .convert import generate_jsonld, process_project
from .scrape import get_all


__all__ = []


INDENT = 2


def arg_setup():
    parser = argparse.ArgumentParser(
        prog="mas2rocrate",
        description="Fetch and/or convert Sigma2 Metacenter (MAS) project data to ro-crates",
    )
    parser.add_argument(
        '-i', '--indent',
        action="store_const",
        const=INDENT,
        help="Indent outputted json by two spaces",
    )
    parser.add_argument(
        '-f', '--fail',
        action='store_true',
        help="Dump original dataset on failure",
    )

    subparsers = parser.add_subparsers(
        help='sub-command help',
        dest='command',
    )

    fetch = subparsers.add_parser('fetch', help='Fetch and convert fetchple projects')
    fetch.add_argument('-e', '--endpoint', help="Use alternative endpoint at URL")
    fetch.add_argument('-u', '--username', help="Authenticate with username")
    fetch.add_argument('-t', '--token', help="Authenticate with token")

    convert = subparsers.add_parser('convert', help='convert file')
    convert.add_argument('json', help="Convert one or more projects in MAS JSON format")
    return parser


def _get_config(args):
    try:
        config = get_config()
    except FileNotFoundError:
        config = Config()
        sys.stderr.write("Config file not found, attempting to continue.\n")
    endpoint = args.endpoint.strip() if args.endpoint else ''
    if endpoint:
        config.ENDPOINT = endpoint
    if not config.ENDPOINT:
        raise ValueError('Missing endpoint')
    username = args.username.strip() if args.username else ''
    if username:
        config.USERNAME = username
    token = args.token.strip() if args.token else ''
    if token:
        config.TOKEN = token
    if not config.is_valid():
        raise ValueError("Missing one of endpoint, username or token. Please add a config-file or use the flags -e, -u and -t.")
    return config


def _get_blobs(args):
    blobs = []
    errors = None
    config = _get_config(args)
    if args.command == 'fetch':
        try:
            blobs = get_all(config.ENDPOINT, config.USERNAME, config.TOKEN)
        except ValueError as e:
            errors = e
    elif args.command == 'convert':
        blobs = json.load(args.json)
        if isinstance(blobs, dict):
            blobs = [blobs]
        elif isinstance(blobs, list):
            pass
        else:
            raise ValueError('Wrong format for input')

    return blobs, errors


def main():
    parser = arg_setup()
    args = parser.parse_args()
    if not args.command:
        parser.print_usage()
        sys.exit(1)

    try:
        blobs, errors = _get_blobs(args)
    except ValueError as e:
        sys.stderr.write(str(e))
        sys.exit(1)

    if errors:
        sys.stderr.write(errors)

    if not blobs:
        sys.stderr.write('Nothing to convert\n')
        sys.exit(1)

    crates = []
    for project in blobs:
        try:
            crate = generate_jsonld(*process_project(project))
        except KeyError as e:
            if args.fail:
                sys.stderr.write(json.dumps(blobs, indent=INDENT) + '\n')
                sys.stderr.write(e)
                sys.stderr.write('\n')
        else:
            crates.append(crate)
    sys.stdout.write(json.dumps(crates, indent=args.indent) + '\n')
    sys.exit()
