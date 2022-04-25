import os
import requests
import logging.config
from page_loader.preparing_html import prepare_html
from page_loader.saving_html import save_html

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def download(url, dir_path=os.getcwd()):
    if os.path.exists(dir_path):
        pass
    else:
        logger.error('Directory not exists!')
        raise OSError
    logger.info('Start to download requested page.')
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError('A 4XX client error or 5XX server error response!')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Can not connect to server!')
    html_content = r.text
    ch_html, page_path = prepare_html(html_content, url, dir_path)
    save_html(page_path, ch_html)
    logger.info('Done!')
    return page_path
