import os
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
    path_to_file = download(args.output, args.page_url)
    print(path_to_file)
