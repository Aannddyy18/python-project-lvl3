import os
import logging.config
from urllib.parse import urljoin
from page_loader.url import normalize_string
from page_loader.url import get_base_url
from page_loader.url import get_base_url_path


logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def filter_tag_attr(img, attrib, base_url):
    _link_ = img.get(attrib)
    base_url_, url_path_ = get_base_url(_link_)
    if base_url_ == base_url \
            or base_url_ == '://':
        return True


def find_resource(bs, base_url, net_loc, page_folder, page_folder_name):
    tag_list = []
    filtered_list = []
    tag_list.extend(bs.find_all(['img', 'script'], src=True))
    tag_list.extend(bs.find_all('link', href=True))
    for tag in tag_list:
        if filter_tag_list(tag, base_url):
            filtered_list.append(tag)
    link_dict = dict.fromkeys(filtered_list)
    for tag in link_dict:
        attrib = define_attr(tag)
        link = tag.get(attrib)
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
        link_dict[tag] = (_link, full_filepath, filepath)
    return link_dict


def filter_tag_list(tag, base_url):
    _link_ = ''
    if (tag == 'img' or tag == 'script') and tag.has_attr('src'):
        _link_ = tag.get('src')
    if tag == 'link' and tag.has_attr('href'):
        _link_ = tag.get('href')
    base_url_, url_path_ = get_base_url(_link_)
    if base_url_ == base_url \
            or base_url_ == '://':
        return True


def define_attr(tag):
    attrib = ''
    if tag.has_attr('src'):
        attrib = 'src'
    if tag.has_attr('href'):
        attrib = 'href'
    return attrib
