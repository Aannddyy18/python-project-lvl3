import os
import requests
import logging.config
from progress.bar import IncrementalBar

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def get_resource(res_url, f_name):
    logger.info('Getting resourses for that page..')
    try:
        r = requests.get(res_url, stream=True)
        r.raise_for_status()
        output_dir = os.path.dirname(f_name)
        os.makedirs(output_dir, exist_ok=True)
        with open(f_name, "wb") as s:
            for line in IncrementalBar('Downloading').iter(r.iter_content()):
                if line:
                    s.write(line)
                    s.flush()
        return True
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError, OSError) as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
        return False


def get_html_content(url):
    logger.info('Start to download requested page.')
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError('A 4XX client error or 5XX server error response!')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Can not connect to server!')
    html_content = r.text
    return html_content
