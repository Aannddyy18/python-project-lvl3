import os
import re
from urllib.parse import urljoin
from page_loader.getting_resourse import get_resourse
from page_loader.getting_base_url import get_base_url
from page_loader.getting_base_url import get_base_url_path


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
                if get_resourse(_link, full_filepath):
                    img[attrib] = filepath


def filter_tag_attr(img, attrib, base_url):
    _link_ = img.get(attrib)
    base_url_, url_path_ = get_base_url(_link_)
    if base_url_ == base_url \
            or base_url_ == '://':
        return True


def normalize_string(string):
    string_name = re.sub('[^a-z0-9]', '-', string)
    return string_name
