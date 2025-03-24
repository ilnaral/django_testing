from http import HTTPStatus

from django.contrib.auth import get_user_model

from .common import URLS, BaseTestCase

User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_pages_availability(self):
        public_urls = (
            URLS["notes_home"],
            URLS["users_login"],
            URLS["users_signup"],
        )
        for url in public_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        auth_urls = (
            URLS["notes_list"],
            URLS["notes_success"],
            URLS["notes_add"],
        )
        for url in auth_urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.auth_user_client, HTTPStatus.NOT_FOUND),
        )
        private_urls = (
            URLS["notes_detail"](self.note.slug),
            URLS["notes_edit"](self.note.slug),
            URLS["notes_delete"](self.note.slug),
        )
        for user, status in users_statuses:
            for url in private_urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        login_url = URLS["users_login"]
        urls = (
            (URLS["notes_list"], None),
            (URLS["notes_success"], None),
            (URLS["notes_add"], None),
            (URLS["notes_detail"](self.note.slug), None),
            (URLS["notes_edit"](self.note.slug), None),
            (URLS["notes_delete"](self.note.slug), None),
        )
        for url, _ in urls:
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
