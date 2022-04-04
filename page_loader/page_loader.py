import os
import requests
import re


def download(_url: str, dir_path=os.getcwd()):
    cut_url = os.path.split(_url)
    if cut_url[1].endswith(('.pdf', '.html', 'jpg', 'txt')):
        cut_url = os.path.splitext(cut_url[1])
        file_name = re.sub('[^a-z0-9]', '-', cut_url[0])
    else:
        file_name = re.sub('[^a-z0-9]', '-', cut_url[1])
    file_name += '.html'
    file_path = os.path.join(dir_path, file_name)
    r = requests.get('https://google.com')
    with open(file_path, 'wb') as f:
        f.write(r.content)
    return file_path
