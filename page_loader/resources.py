import os
import requests
import logging.config


logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def get_html_content(url):
    logger.info('Start to download requested page.')
    try:
        r = requests.get(url)
        r.raise_for_status()
        html_content = r.text
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError('A 4XX client error or 5XX server error response!')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Can not connect to server!')
    return html_content


def get_content(res_url):
    logger.info('Getting content for that page..')
    asset_content = b''
    try:
        r = requests.get(res_url, stream=True)
        r.raise_for_status()
        asset_content = r.content
    except requests.exceptions.RequestException as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
    return asset_content
