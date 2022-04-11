import os
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as B_s


def download(url, dir_path=os.getcwd()):
    o = urlparse(url)
    net_loc = o.netloc
    split_path = os.path.splitext(o.path)
    if split_path[1] == '' and split_path[0] == '':
        page_name = normalize_string(net_loc)
    else:
        page_name = normalize_string(net_loc + split_path[0])
    page_folder_name = page_name + '_files'
    page_name += '.html'
    page_path = os.path.join(dir_path, page_name)
    page_folder = os.path.join(dir_path, page_folder_name)
    html_content = requests.get(url).text
    image_links = parse_rename_image_links(url, page_path, page_folder_name, page_folder, html_content)
    for img_url, f_name in image_links.items():
        img_content = requests.get(img_url).content
        dump_image(f_name, img_content)
    return page_path


def parse_rename_image_links(url, page_path, page_folder_name, page_folder, html_content):
    result = {}
    base_url, net_loc = get_base_url(url)
    bs = B_s(html_content, "html.parser")
    for img in bs.findAll("img"):
        if img.has_attr("src"):
            link = img.get("src")
            _link = urljoin(base_url, link)
            filename, ext = os.path.splitext(link)
            filename = normalize_string(net_loc + filename)
            filename += ext
            filepath = os.path.join(page_folder_name, filename)
            full_filepath = os.path.join(page_folder, filename)
            img['src'] = filepath
            result[_link] = full_filepath
    with open(page_path, 'wb') as file:
        file.write(bs.prettify('utf-8'))
    return result


def get_base_url(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.netloc


def dump_image(output_path, content):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as s:
        s.write(content)


def normalize_string(string):
    string_name = re.sub('[^a-z0-9]', '-', string)
    return string_name
