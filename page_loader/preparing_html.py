import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup as B_s
from page_loader.normalizing_string import normalize_string
from page_loader.getting_resourse import get_resourse
from page_loader.getting_base_url import get_base_url
from page_loader.charging_soup import charge_soup


def prepare_html(html: str, url: str, dir_path):
    o = urlparse(url)
    base_url, net_loc = get_base_url(url)
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(net_loc)
    else:
        page_name = normalize_string(net_loc + split_path[0])
    page_folder_name = page_name + '_files'
    page_name += '.html'
    page_path = os.path.join(dir_path, page_name)
    page_folder = os.path.join(dir_path, page_folder_name)
    html_page_path = os.path.join(page_folder_name, page_name)
    _bs = B_s(html, "html.parser")
    charge_soup(_bs, base_url, net_loc, page_folder, page_folder_name)
    changed_html = _bs.prettify('utf-8')
    get_resourse(url, html_page_path)
    return changed_html, page_path, html_page_path
