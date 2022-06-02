import os
import requests
import logging.config
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from page_loader.url import get_base_url
from page_loader.url import form_page_name
from page_loader.url import make_file_name
from page_loader.url import form_folder_name
from page_loader.resources import get_html_content
from page_loader.resources import get_content
from page_loader.html import find_resources
from page_loader.html import change_tag_link
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
            requests.exceptions.ConnectionError) as exception:
        error_text = type(exception).__name__ + ": " + str(exception)
        logger.warning('Fail to download, error happens: ' + error_text)
        raise

    page_folder_name = form_folder_name(url)
    page_name = form_page_name(url)
    base_url, net_loc = get_base_url(url)
    page_path = os.path.join(dir_path, page_name)
    page_folder = os.path.join(dir_path, page_folder_name)
    html_page_path = os.path.join(page_folder_name, page_name)
    parsed_html = BeautifulSoup(html_content, "html.parser")
    tag_to_link_dict = find_resources(parsed_html, base_url)

    bar_width = len(tag_to_link_dict)

    with IncrementalBar("Downloading:", max=bar_width) as bar:
        bar.suffix = "%(percent).1f%% (eta: %(eta)s)"

        for tag, local_asset_absolute_url in tag_to_link_dict.items():
            try:
                asset_file_content = get_content(local_asset_absolute_url)
            except requests.exceptions.RequestException as exception:
                error_text = type(exception).__name__ + ": " + str(exception)
                logger.warning('Fail to download, error happens: ' + error_text)
                continue
            asset_file_name = make_file_name(local_asset_absolute_url, net_loc)
            full_asset_file_name = os.path.join(page_folder, asset_file_name)
            save_resource(full_asset_file_name, asset_file_content)
            relative_path_to_asset = os.path.join(page_folder_name, asset_file_name)
            change_tag_link(tag, relative_path_to_asset)
            bar.next()

        changed_html = parsed_html.prettify('utf-8')
        save_resource(page_path, changed_html)
        save_resource(html_page_path, changed_html)
        logger.info('Done!')
    return page_path
