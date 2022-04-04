import os
from os.path import dirname
import tempfile
import requests_mock
from page_loader.scripts.pageloader import download


FIXTURES_FOLDER = 'fixtures'


def get_content(path_to_file):
    with open(path_to_file, "rb") as f:
        return f.read()


expected_result = get_content(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'expected_page.html'))


def test_page_loader_content():
    with requests_mock.Mocker() as m:
        m.get('https://google.com', content=expected_result)
        with tempfile.TemporaryDirectory() as tmpdirname:
            download('https://google.com', tmpdirname)
            with open(os.path.join(tmpdirname, "google-com.html"), 'rb') as d:
                downloaded_content = d.read()
                assert downloaded_content == expected_result


def test_page_loader_path_to_file():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_path = download('https://google.com', tmpdirname)
        expected_path = os.path.join(tmpdirname, "google-com.html")
        assert actual_path == expected_path
