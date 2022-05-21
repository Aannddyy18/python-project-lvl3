import os
import re
from urllib.parse import urlparse


def form_folder_name(url):
    o = urlparse(url)
    base_url, net_loc = get_base_url(url)
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(net_loc)
    else:
        page_name = normalize_string(net_loc + split_path[0])
    page_folder_name = page_name + '_files'
    return page_folder_name


def form_page_name(url):
    o = urlparse(url)
    base_url, net_loc = get_base_url(url)
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(net_loc)
    else:
        page_name = normalize_string(net_loc + split_path[0])
    page_name += '.html'
    return page_name


def get_base_url(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.netloc


def get_base_url_path(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.path


def normalize_string(string):
    string_name = re.sub('[^a-z0-9]', '-', string)
    return string_name
