from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .common import URLS, BaseTestCase


class TestRoutes(BaseTestCase):

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        expected_note_count = Note.objects.count()
        response = self.author_client.post(URLS["notes_add"], data=self.data)
        self.assertRedirects(response, URLS["notes_success"])
        self.assertEqual(Note.objects.count(), expected_note_count + 1)
        new_note = Note.objects.get(slug=self.data["slug"])
        self.assertEqual(new_note.title, self.data["title"])
        self.assertEqual(new_note.text, self.data["text"])
        self.assertEqual(new_note.slug, self.data["slug"])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        expected_note_count = Note.objects.count()
        response = self.client.post(URLS["notes_add"], self.data)
        expected_url = f'{URLS["users_login"]}?next={URLS["notes_add"]}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), expected_note_count)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        expected_note_count = Note.objects.count()
        response = self.author_client.post(URLS["notes_add"], data={
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": self.note.slug
        })
        self.assertFormError(response, "form", "slug", errors=(self.note.slug
                                                               + WARNING))
        self.assertEqual(Note.objects.count(), expected_note_count)

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.
        """
        expected_note_count = Note.objects.count()
        data_without_slug = {
            "title": "Новый заголовок",
            "text": "Новый текст",
        }
        response = self.author_client.post(URLS["notes_add"],
                                           data=data_without_slug)
        self.assertRedirects(response, URLS["notes_success"])
        self.assertEqual(Note.objects.count(), expected_note_count + 1)
        new_note = Note.objects.get(title=data_without_slug["title"])
        expected_slug = slugify(data_without_slug["title"])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_delete_note(self):
        """Пользователь может удалять свои заметки."""
        expected_note_count = Note.objects.count()
        response = self.author_client.post(URLS["notes_delete"]
                                           (self.note.slug))
        self.assertRedirects(response, URLS["notes_success"])
        self.assertEqual(Note.objects.count(), expected_note_count - 1)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_client.post(URLS["notes_edit"](self.note.slug),
                                           data=self.data)
        self.assertRedirects(response, URLS["notes_success"])
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.data["title"])
