import os
import sys
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def save_change(soup, net_loc, pagefolder, url, tag, inner):
    if not os.path.exists(pagefolder):  # create only once
       try:
            os.mkdir(pagefolder)
       except Exception as exc:
           print(exc, file=sys.stderr)
    for res in soup.findAll(tag):  # images
        if res.has_attr(inner):  # check inner tag
            try:
                fileurl = urljoin(url, res.get(inner))
                filename, ext = os.path.splitext(res[inner])  # get name and extension
                filename = re.sub('[^a-z0-9]', '-', net_loc + filename) + ext
                filepath = os.path.join(pagefolder, filename)
                # rename html ref
                res[inner] = os.path.join(pagefolder, filename)
                if not os.path.isfile(filepath):  # was not downloaded
                    with open(filepath, 'wb') as file:
                        session = requests.Session()
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)


def download(url, dir_path=os.getcwd()):
    o = urlparse(url)
    net_loc = o.netloc
    split_path = os.path.splitext(o.path)
    cut_url = os.path.split(url)
    if split_path[1] != '':
        cut_url = os.path.splitext(cut_url[1])
        page_name = re.sub('[^a-z0-9]', '-', (net_loc + '/' + cut_url[0]))
    elif split_path[1] == '' and split_path[0] == '':
        page_name = re.sub('[^a-z0-9]', '-', net_loc)
    else:
        page_name = re.sub('[^a-z0-9]', '-', (net_loc + '/' + cut_url[1]))
    pagefolder = page_name + '_files'
    page_name += '.html'
    file_path = os.path.join(dir_path, page_name)
    session = requests.Session()
    responce = session.get(url)
    soup = BeautifulSoup(responce.text, "html.parser")
    tags_inner = {'img': 'src'}
    for tag, inner in tags_inner.items(): # saves resource files and rename refs
        save_change(soup, net_loc, pagefolder, url, tag, inner)
    with open(page_name, 'wb') as file: # saves modified html doc
        file.write(soup.prettify('utf-8'))
    return file_path