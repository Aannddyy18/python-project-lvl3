import os
from os.path import dirname
import tempfile
import requests
import requests_mock
from bs4 import BeautifulSoup
from page_loader.scripts.pageloader import download
from page_loader.page_loader import save_change

FIXTURES_FOLDER = 'fixtures'


def get_content(path_to_file):
    with open(path_to_file, "r") as f:
        return f.read()


def get_content_b(path_to_file):
    with open(path_to_file, "rb") as f:
        return f.read()


expected_result = get_content(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'expected_page.html'))
source_page = get_content(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'source_page.html'))
expected_image = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'hexlet.png'))
changed_page = get_content(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'changed_page.html'))


def test_page_loader_path_to_file():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_path = download('https://google.com', tmpdirname)
        expected_path = os.path.join(tmpdirname, "google-com.html")
        assert actual_path == expected_path


def test_page_loader_img():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses/assets/professions/nodejs.png', content=expected_image)
        with tempfile.TemporaryDirectory():
            soup = BeautifulSoup(source_page, "html.parser")
            url = 'https://ru.hexlet.io/courses'
            net_loc = 'ru.hexlet.io'
            save_change(
                        soup, net_loc, 'ru-hexlet-io-courses_files', url, 'img', 'src')
            with open(
                        os.path.join('ru-hexlet-io-courses_files',
                                    'ru-hexlet-io-assets-professions-nodejs.png'
                                    ), 'rb') as d:
                downloaded_content = d.read()
                assert downloaded_content == expected_image


def test_page_loader_change():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=source_page)
        with tempfile.TemporaryDirectory() as tmpdirname:
            download('https://ru.hexlet.io/courses', tmpdirname)
            with open(
                    os.path.join('ru-hexlet-io-courses.html'), 'r') as d:
                downloaded_content = d.read()
                assert downloaded_content == changed_page
