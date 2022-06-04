import os
import logging.config
from urllib.parse import urljoin
from page_loader.url import get_base_url


logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


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
    tag_list.extend(bs.find_all(['img', 'script'], src=True))
    tag_list.extend(bs.find_all('link', href=True))
    local_res_dict = {}
    for tag in tag_list:
        attrib = define_attr(tag)
        link = tag.get(attrib)
        base_link_url, net_loc = get_base_url(link)
        if base_link_url == base_url:
            local_res_dict[tag] = link
        elif base_link_url == "://":
            link = urljoin(base_url, link)
            local_res_dict[tag] = link
    return local_res_dict
