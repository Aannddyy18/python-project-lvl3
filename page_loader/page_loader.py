import os
import requests
import logging.config
from bs4 import BeautifulSoup
from page_loader.url import get_base_url
from page_loader.url import form_page_name
from page_loader.url import form_folder_name
from page_loader.resources import get_html_content
from page_loader.html import find_resource
from page_loader.resources import try_to_get_resource
from page_loader.resources import change_attributes
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

    page_folder_name = form_folder_name(url)
    page_name = form_page_name(url)
    base_url, net_loc = get_base_url(url)
    page_path = os.path.join(dir_path, page_name)
    page_folder = os.path.join(dir_path, page_folder_name)
    html_page_path = os.path.join(page_folder_name, page_name)
    _bs = BeautifulSoup(html_content, "html.parser")
    links_dict = find_resource(_bs, base_url, net_loc, page_folder, page_folder_name)
    success_res_dict = try_to_get_resource(links_dict, page_folder_name)
    change_attributes(links_dict, success_res_dict)
    changed_html = _bs.prettify('utf-8')
    save_resource(page_path, changed_html)
    save_resource(html_page_path, changed_html)
    logger.info('Done!')
    return page_path
