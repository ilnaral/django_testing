from http import HTTPStatus
from pytest_django.asserts import assertRedirects

HTTP_OK = HTTPStatus.OK
HTTP_NOT_FOUND = HTTPStatus.NOT_FOUND


def get_login_redirect_url(url, login_url):
    return f'{login_url}?next={url}'


def assert_redirects(response, expected_url):
    assertRedirects(response, expected_url)
