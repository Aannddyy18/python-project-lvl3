import os
import pytest
from os.path import dirname
import requests
import requests_mock
from page_loader.__main__ import download

FIXTURES_FOLDER = 'fixtures'


def get_content(path_to_file):
    with open(path_to_file, "r") as f:
        return f.read()


def get_content_b(path_to_file):
    with open(path_to_file, "rb") as f:
        return f.read()


source_page = get_content(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'source_page.html'))
expected_image = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'hexlet.png'))
changed_page = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'changed_page.html'))
expected_css = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'application.css'))
expected_js = get_content_b(os.path.join(dirname(__file__), FIXTURES_FOLDER, 'runtime.js'))
image_path = os.path.join('ru-hexlet-io-courses_files',
                          'ru-hexlet-io-assets-professions-nodejs.png')
html_page_path = os.path.join('ru-hexlet-io-courses.html')
css_path = os.path.join('ru-hexlet-io-courses_files',
                        'ru-hexlet-io-assets-application.css')
js_path = os.path.join('ru-hexlet-io-courses_files',
                       'ru-hexlet-io-packs-js-runtime.js')

test_requests_data = [
    (image_path, expected_image), (css_path, expected_css),
    (html_page_path, changed_page), (js_path, expected_js)
]

test_errors_data = [
    ('http://twitter.com/api/1/foobar', requests.exceptions.ConnectionError, 'Can not connect to server!'),
    ('http://instagram.com/api/1/foobar', requests.exceptions.HTTPError,
     'A 4XX client error or 5XX server error response!')
]


def test_page_loader_path_to_file(tmpdir):
    actual_path = download('https://ru.hexlet.io/courses', tmpdir)
    expected_path = os.path.join(tmpdir, "ru-hexlet-io-courses.html")
    assert actual_path == expected_path


@pytest.mark.parametrize("path, expected", test_requests_data)
@requests_mock.Mocker(kw='mock')
def test_page_loader_img(path, expected, tmpdir, **kwargs):
    kwargs['mock'].get('https://ru.hexlet.io/courses', text=source_page)
    kwargs['mock'].get('https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_image)
    kwargs['mock'].get('https://ru.hexlet.io/assets/application.css', content=expected_css)
    kwargs['mock'].get('https://ru.hexlet.io/packs/js/runtime.js', content=expected_js)
    download('https://ru.hexlet.io/courses', tmpdir)
    with open(
            os.path.join(tmpdir, path), 'rb') as d:
        downloaded_content = d.read()
        assert downloaded_content == expected


def test_page_loader_os_error_exceptions(tmpdir):
    with pytest.raises(OSError) as e:
        os.chmod(tmpdir, 0o444)
        download('https://ru.hexlet.io/courses', tmpdir)
    assert str(e.value) == 'Can not save requested page!'


@pytest.mark.parametrize("str_url, error, str_error", test_errors_data)
@requests_mock.Mocker(kw='mock')
def test_page_loader_connection_errors(str_url, error, str_error, tmpdir, **kwargs):
    kwargs['mock'].get(str_url, exc=error)
    with pytest.raises(error) as e:
        download(str_url, tmpdir)
        assert str(e.value) == str_error
