import os
from os.path import dirname
import tempfile
import requests_mock
from page_loader.scripts.pageloader import download

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
expected_css = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'application.css'))
expected_js = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'runtime.js'))


def test_page_loader_path_to_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        actual_path = download('https://ru.hexlet.io/courses', tmp_dir)
        expected_path = os.path.join(tmp_dir, "ru-hexlet-io-courses.html")
        assert actual_path == expected_path


def test_page_loader_img():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=source_page)
        m.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_image)
        m.get('https://ru.hexlet.io/assets/application.css', content=expected_css)
        m.get('https://ru.hexlet.io/packs/js/runtime.js', content=expected_js)
        with tempfile.TemporaryDirectory() as tmp_dir:
            download('https://ru.hexlet.io/courses', tmp_dir)
            with open(
                    os.path.join(tmp_dir, 'ru-hexlet-io-courses_files',
                                 'ru-hexlet-io-assets-professions-nodejs.png'
                                 ), 'rb') as d:
                downloaded_content = d.read()
                assert downloaded_content == expected_image


def test_page_loader_change():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=source_page)
        m.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_image)
        m.get('https://ru.hexlet.io/assets/application.css', content=expected_css)
        m.get('https://ru.hexlet.io/packs/js/runtime.js', content=expected_js)
        with tempfile.TemporaryDirectory() as tmp_dir:
            download('https://ru.hexlet.io/courses', tmp_dir)
            with open(
                    os.path.join(tmp_dir, 'ru-hexlet-io-courses.html'), 'r') as d:
                downloaded_content = d.read()
                assert downloaded_content == changed_page


def test_page_loader_css():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=source_page)
        m.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_image)
        m.get('https://ru.hexlet.io/assets/application.css', content=expected_css)
        m.get('https://ru.hexlet.io/packs/js/runtime.js', content=expected_js)
        with tempfile.TemporaryDirectory() as tmp_dir:
            download('https://ru.hexlet.io/courses', tmp_dir)
            with open(
                    os.path.join(tmp_dir, 'ru-hexlet-io-courses_files',
                                 'ru-hexlet-io-assets-application.css'
                                 ), 'rb') as d:
                downloaded_content = d.read()
                assert downloaded_content == expected_css


def test_page_loader_js():
    with requests_mock.Mocker() as m:
        m.get('https://ru.hexlet.io/courses', text=source_page)
        m.get('https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_image)
        m.get('https://ru.hexlet.io/assets/application.css', content=expected_css)
        m.get('https://ru.hexlet.io/packs/js/runtime.js', content=expected_js)
        with tempfile.TemporaryDirectory() as tmp_dir:
            download('https://ru.hexlet.io/courses', tmp_dir)
            with open(
                    os.path.join(tmp_dir, 'ru-hexlet-io-courses_files',
                                 'ru-hexlet-io-packs-js-runtime.js'
                                 ), 'rb') as d:
                downloaded_content = d.read()
                assert downloaded_content == expected_js
