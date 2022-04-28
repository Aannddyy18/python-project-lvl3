import os
import requests
import logging.config
from progress.bar import IncrementalBar

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger()


def get_resourse(res_url, f_name):
    logger.info('Getting resourses for that page..')
    try:
        r = requests.get(res_url, stream=True)
        r.raise_for_status()
        output_dir = os.path.dirname(f_name)
        os.makedirs(output_dir, exist_ok=True)
        with open(f_name, "wb") as s:
            for line in IncrementalBar('Downloading').iter(r.iter_content()):
                if line:
                    s.write(line)
                    s.flush()
        return True
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError, OSError) as e:
        error_text = type(e).__name__ + ": " + str(e)
        logger.warning('Fail to download, error happens: ' + error_text)
        return False


def save_html(file_path, file_name):
    try:
        with open(file_path, 'wb') as file:
            file.write(file_name)
    except OSError:
        raise OSError("Can not save requested page!")
    