from http import HTTPStatus

from django.test import TestCase

HTTP_OK = HTTPStatus.OK
HTTP_NOT_FOUND = HTTPStatus.NOT_FOUND


def assert_redirects_to_comments(response, news_detail_url):
    """Проверка редиректа на страницу с комментариями."""
    expected_url = f"{news_detail_url}#comments"
    TestCase().assertRedirects(response, expected_url)


def assert_not_found(response):
    """Проверка статуса HTTP_NOT_FOUND."""
    TestCase().assertEqual(response.status_code, HTTP_NOT_FOUND)
