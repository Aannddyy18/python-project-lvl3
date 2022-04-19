import os
import sys
import logging
import requests
import argparse
import pathlib
from page_loader.page_loader import download


def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('page_url', metavar='url_for_page')
    parser.add_argument(
        '-o', '--output', default=os.getcwd(), type=pathlib.Path,
        help='set path to existing directory for download'
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_command_line_args()
    try:
        path_to_file = download(args.page_url, args.output)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to connect to server, reason: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download by a link, reason: {e}")
        sys.exit(1)
    except OSError as e:
        logging.error(f"Failed to save, reason: {e}")
        sys.exit(1)
    print(path_to_file)


if __name__ == "__main__":
    main()
