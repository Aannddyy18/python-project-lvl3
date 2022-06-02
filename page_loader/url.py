import os
import re
from urllib.parse import urlparse


def form_folder_name(url):
    o = urlparse(url)
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(o.netloc)
    else:
        page_name = normalize_string(o.netloc + split_path[0])
    page_folder_name = page_name + '_files'
    return page_folder_name


def form_page_name(url):
    o = urlparse(url)
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(o.netloc)
    else:
        page_name = normalize_string(o.netloc + split_path[0])
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


def make_file_name(link, net_loc):
    url = urlparse(link)
    filename, ext = os.path.splitext(url.path)
    if ext == '':
        ext = '.html'
    filename = normalize_string(net_loc + filename)
    filename += ext
    return filename
