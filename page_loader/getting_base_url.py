from urllib.parse import urlparse


def get_base_url(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.netloc


def get_base_url_path(page_url):
    url = urlparse(page_url)
    return f"{url.scheme}://{url.netloc}", url.path
