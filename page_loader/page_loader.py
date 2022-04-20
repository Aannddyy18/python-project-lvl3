import os
import sys
import logging
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as B_s
from progress.bar import IncrementalBar


def download(url, dir_path=os.getcwd()):
    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(logging.INFO)
    stderr.setFormatter(formatter)
    stdout.setFormatter(formatter)
    logging.basicConfig(handlers=[stdout, stderr])
    logging.info('Start to download requested page.')
    r = requests.get(url)
    html_content = r.text
    ch_html, html_links, page_path = prepare_html(html_content, url, dir_path)
    save_html(page_path, ch_html)
    get_res(html_links)
    logging.info('Done!')
    return page_path


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

    _bs = B_s(html, "html.parser")

    def charge_soup(bs):
        _result = {}
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
                    img[attrib] = filepath
                    _result[_link] = full_filepath
        return _result

    def filter_tag_attr(img, attrib):
        _link_ = img.get(attrib)
        base_url_, url_path_ = get_base_url(_link_)
        if base_url_ == 'https://ru.hexlet.io' \
                or base_url_ == '://':
            return True

    result = charge_soup(_bs)
    changed_html = _bs.prettify('utf-8')
    return changed_html, result, page_path


def save_html(file_path, file_name):
    with open(file_path, 'wb') as file:
        file.write(file_name)


def get_res(res_dict):
    for res_url, f_name in res_dict.items():
        logging.info('Getting resourses for that page..')
        r = requests.get(res_url, stream=True)
        output_dir = os.path.dirname(f_name)
        os.makedirs(output_dir, exist_ok=True)
        with open(f_name, "wb") as s:
            for line in IncrementalBar('Downloading').iter(r.iter_content()):
                if line:
                    s.write(line)
                    s.flush()


def get_base_url(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.netloc


def get_base_url_path(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.path


def dump_res(output_path, content):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as s:
        s.write(content)


def normalize_string(string):
    string_name = re.sub('[^a-z0-9]', '-', string)
    return string_name
