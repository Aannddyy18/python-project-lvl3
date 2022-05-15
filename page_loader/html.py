import os
import requests
import logging.config
from urllib.parse import urljoin
from page_loader.resources import get_resource
from page_loader.url import normalize_string
from page_loader.url import get_base_url
from page_loader.url import get_base_url_path
from page_loader.url import form_names
from bs4 import BeautifulSoup


logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def prepare_html(html: str, url: str, dir_path):
    page_folder_name, page_name = form_names(url)
    base_url, net_loc = get_base_url(url)
    page_path = os.path.join(dir_path, page_name)
    page_folder = os.path.join(dir_path, page_folder_name)
    html_page_path = os.path.join(page_folder_name, page_name)
    _bs = BeautifulSoup(html, "html.parser")
    charge_soup(_bs, base_url, net_loc, page_folder, page_folder_name)
    changed_html = _bs.prettify('utf-8')
    try:
        get_resource(url, html_page_path)
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError, OSError) as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
        raise
    return changed_html, page_path


def charge_soup(bs, base_url, net_loc, page_folder, page_folder_name):
    tags = ["img", "link", "script"]
    for img in bs.find_all(tags):
        attribs = ['src', 'href']
        for attrib in attribs:
            if filter_tag_attr(img, attrib, base_url):
                link = img.get(attrib)
                base_link_url, link_path = get_base_url_path(link)
                _link = ''
                if base_link_url == base_url:
                    _link = link
                elif base_link_url == "://":
                    _link = urljoin(base_url, link)
                filename, ext = os.path.splitext(link_path)
                if ext == '':
                    ext = '.html'
                filename = normalize_string(net_loc + filename)
                filename += ext
                filepath = os.path.join(page_folder_name, filename)
                full_filepath = os.path.join(page_folder, filename)
                if get_resource(_link, full_filepath):
                    img[attrib] = filepath


def filter_tag_attr(img, attrib, base_url):
    _link_ = img.get(attrib)
    base_url_, url_path_ = get_base_url(_link_)
    if base_url_ == base_url \
            or base_url_ == '://':
        return True
