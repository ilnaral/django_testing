from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

LOGIN_URL = pytest.lazy_fixture('login_url') # type: ignore
LOGOUT_URL = pytest.lazy_fixture('logout_url') # type: ignore
SIGNUP_URL = pytest.lazy_fixture('signup_url') # type: ignore
DETAIL_URL = pytest.lazy_fixture('news_detail_url') # type: ignore
EDIT_URL = pytest.lazy_fixture('comment_edit_url') # type: ignore
DELETE_URL = pytest.lazy_fixture('comment_delete_url') # type: ignore
HOME_URL = pytest.lazy_fixture('news_home_url') # type: ignore


NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client') # type: ignore
ANON_CLIENT = pytest.lazy_fixture('client') # type: ignore
AUTHOR_CLIENT = pytest.lazy_fixture('author_client') # type: ignore

EDIT_DELETE_URLS = (DELETE_URL, EDIT_URL)
ANON_URLS = (DETAIL_URL, HOME_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)

TEST_STATUS_CODES_DATA = [
    (NOT_AUTHOR_CLIENT, url, HTTPStatus.NOT_FOUND)
    for url in EDIT_DELETE_URLS
] + [
    (ANON_CLIENT, url, HTTPStatus.OK)
    for url in ANON_URLS
] + [
    (AUTHOR_CLIENT, url, HTTPStatus.OK)
    for url in EDIT_DELETE_URLS
]


@pytest.mark.parametrize(
    'test_client, url, expected_status',
    TEST_STATUS_CODES_DATA
)
def test_status_codes(test_client, url, expected_status):
    response = test_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('url', EDIT_DELETE_URLS)
def test_redirects(client, url, login_url):
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
