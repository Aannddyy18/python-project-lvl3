import os
import logging.config
from urllib.parse import urljoin
from page_loader.url import get_base_url
from page_loader.url import get_base_url_path

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def filter_tag_list(tag, base_url):
    link_ = ''
    if (tag == 'img' or tag == 'script') and tag.has_attr('src'):
        link_ = tag.get('src')
    elif tag == 'link' and tag.has_attr('href'):
        link_ = tag.get('href')
    base_url_, url_path = get_base_url_path(link_)
    if base_url_ == base_url or base_url_ == '://':
        return True


def define_attr(tag):
    attrib = ''
    if tag.has_attr('src'):
        attrib = 'src'
    if tag.has_attr('href'):
        attrib = 'href'
    return attrib


def change_tag_link(tag, relative_path_to_asset):
    attrib = define_attr(tag)
    tag[attrib] = relative_path_to_asset


def find_resources(bs, base_url):
    tag_list = []
    filtered_list = []
    tag_list.extend(bs.find_all(['img', 'script'], src=True))
    tag_list.extend(bs.find_all('link', href=True))
    for tag in tag_list:
        if filter_tag_list(tag, base_url):
            filtered_list.append(tag)
    local_res_dict = dict.fromkeys(filtered_list)
    for tag in local_res_dict:
        attrib = define_attr(tag)
        link = tag.get(attrib)
        base_link_url, net_loc = get_base_url(link)
        _link = ''
        if base_link_url == base_url:
            _link = link
        elif base_link_url == "://":
            _link = urljoin(base_url, link)
        local_res_dict[tag] = _link
    return local_res_dict
