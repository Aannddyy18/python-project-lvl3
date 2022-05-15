import os
import logging.config
from page_loader.resources import get_html_content
from page_loader.html import prepare_html
from page_loader.storage import save_html

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def download(url, dir_path=os.getcwd()):
    if os.path.exists(dir_path):
        pass
    else:
        logger.error('Directory not exists!')
        raise OSError
    html_content = get_html_content(url)
    ch_html, page_path = prepare_html(html_content, url, dir_path)
    save_html(page_path, ch_html)
    logger.info('Done!')
    return page_path
