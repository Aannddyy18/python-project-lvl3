import os
import requests
import logging.config
from page_loader.resources import get_html_content
from page_loader.html import parse_html
from page_loader.resources import try_to_get_resource
from page_loader.storage import save_resource

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def download(url, dir_path=os.getcwd()):
    if os.path.exists(dir_path):
        pass
    else:
        logger.error('Directory not exists!')
        raise OSError
    try:
        html_content = get_html_content(url)
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
        raise
    _bs, links_dict, page_path, html_page_path, page_folder_name = parse_html(html_content, url, dir_path)
    try_to_get_resource(links_dict, page_folder_name)
    changed_html = _bs.prettify('utf-8')
    save_resource(page_path, changed_html)
    save_resource(html_page_path, changed_html)
    logger.info('Done!')
    return page_path
