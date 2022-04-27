import os
import sys
import requests
import argparse
import pathlib
import logging.config
from page_loader.page_loader import download

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


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
    except requests.exceptions.HTTPError as e:
        print(f"Failed to connect to server {e.request.url}, "
              f"code {e.response.status_code} was returned")
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        error_text = type(e).__name__ + ": " + str(e)
        print(f"Failed to load from {e.request.url}, error happens: {error_text}")
        sys.exit(1)
    except OSError as e:
        error_text = type(e).__name__ + ": " + str(e)
        print(f"Failed to save file, error happens: {error_text}")
        sys.exit(1)
    except BaseException as e:
        error_text = type(e).__name__ + ": " + str(e)
        print(f"Unexpected error happens: {error_text}")
        sys.exit(1)
    print(path_to_file)


if __name__ == "__main__":
    main()
