import os
from progress.bar import IncrementalBar
import requests
import logging.config
from page_loader.html import define_attr
from page_loader.storage import save_resource


logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def get_resource(res_url, page_folder_name):
    logger.info('Getting resources for that page..')
    try:
        r = requests.get(res_url, stream=True)
        r.raise_for_status()
        save_resource(page_folder_name, r.content)
        return True
    except (requests.exceptions.RequestException, OSError) as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
        return False
    except OSError:
        raise


def try_to_get_resource(links_dict, page_folder_name):
    if not links_dict:
        return
    if not os.path.exists(page_folder_name):
        try:
            logger.info('Create directory for resources: %s', page_folder_name)
            os.makedirs(page_folder_name, exist_ok=True)
        except OSError:
            raise OSError('Can not save requested page!')

    bar_width = len(links_dict)
    success_res_dict = {}

    with IncrementalBar("Downloading:", max=bar_width) as bar:
        bar.suffix = "%(percent).1f%% (eta: %(eta)s)"

        for tag, v in links_dict.items():
            attrib = define_attr(tag)
            if get_resource(v[0], v[1]):
                success_res_dict[tag[attrib]] = v[2]
            bar.next()

    return success_res_dict


def change_attributes(links_dict, success_res_dict):
    for tag in links_dict.keys():
        attrib = define_attr(tag)
        if tag[attrib] in success_res_dict:
            tag[attrib] = success_res_dict[tag[attrib]]


def get_html_content(url):
    logger.info('Start to download requested page.')
    try:
        r = requests.get(url)
        r.raise_for_status()
        html_content = r.text
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError('A 4XX client error or 5XX server error response!')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Can not connect to server!')
    return html_content
