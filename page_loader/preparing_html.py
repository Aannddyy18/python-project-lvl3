import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as B_s
from page_loader.normalizing_string import normalize_string
from page_loader.getting_resourse import get_resourse
from page_loader.getting_base_url import get_base_url
from page_loader.getting_base_url import get_base_url_path


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

    def charge_soup(bs):
        tags = ["img", "link", "script"]
        for img in bs.find_all(tags):
            attribs = ['src', 'href']
            for attrib in attribs:
                if filter_tag_attr(img, attrib):
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
                    if get_resourse(_link, full_filepath):
                        img[attrib] = filepath

    def filter_tag_attr(img, attrib):
        _link_ = img.get(attrib)
        base_url_, url_path_ = get_base_url(_link_)
        if base_url_ == base_url \
                or base_url_ == '://':
            return True

    charge_soup(_bs)
    changed_html = _bs.prettify('utf-8')
    return changed_html, page_path, html_page_path
