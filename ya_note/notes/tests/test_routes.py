from http import HTTPStatus

from django.contrib.auth import get_user_model

from .common import URLS, BaseTestCase

User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_pages_availability(self):
        """Потому что я дурашка невнимательная."""
        self.anon_urls = (
            self.home_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        self.auth_user_urls = (
            self.notes_list_url,
            self.add_url,
            self.success_url,
        )
        self.diff_users_urls = (
            self.detail_url,
            self.edit_url,
            self.delete_url,
        )
        self.test_status_code_data = (
            (
                self.client,
                self.anon_urls,
                HTTPStatus.OK
            ),
            (
                self.not_author_client,
                self.auth_user_urls,
                HTTPStatus.OK
            ),
            (
                self.author_client,
                self.diff_users_urls,
                HTTPStatus.OK
            ),
            (
                self.not_author_client,
                self.diff_users_urls,
                HTTPStatus.NOT_FOUND
            ),
        )

        for client, urls, expected_status_code in self.test_status_code_data:
            for url in urls:
                with self.subTest(
                    client=client,
                    url=url,
                    expected_status_code=expected_status_code
                ):
                    response = client.get(url)
                    self.assertEqual(
                        response.status_code, expected_status_code
                    )

    def test_redirects(self):
        login_url = URLS["users_login"]
        note_slug = self.note.slug
        urls = [
            URLS["notes_list"],
            URLS["notes_success"],
            URLS["notes_add"],
            URLS["notes_detail"](note_slug),
            URLS["notes_edit"](note_slug),
            URLS["notes_delete"](note_slug),
        ]

        for url in urls:
            with self.subTest(url=url):
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
