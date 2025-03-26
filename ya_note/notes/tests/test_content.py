from django.contrib.auth import get_user_model

from notes.forms import NoteForm

from .common import URLS, BaseTestCase

User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_notes_list_for_different_users(self):
        """
        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context.
        Не допускается попадание заметки другого пользователя.
        """
        users_statuses = (
            (self.author_client, True),
            (self.not_author_client, False),
        )
        for user, note_in_list in users_statuses:
            with self.subTest():
                response = user.get(URLS["notes_list"])
                object_list = response.context["object_list"]
                self.assertIs((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (
            (URLS["notes_add"], None),
            (URLS["notes_edit"](self.note.slug), None),
        )
        for url, _ in urls:
            with self.subTest():
                response = self.author_client.get(url)
                form = response.context['form']
                self.assertIsInstance(form, NoteForm)
