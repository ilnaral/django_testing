from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

URLS = {
    "notes_list": reverse("notes:list"),
    "notes_add": reverse("notes:add"),
    "notes_edit": lambda slug: reverse("notes:edit", args=(slug,)),
    "notes_delete": lambda slug: reverse("notes:delete", args=(slug,)),
    "notes_detail": lambda slug: reverse("notes:detail", args=(slug,)),
    "notes_success": reverse("notes:success"),
    "users_login": reverse("users:login"),
    "notes_home": reverse("notes:home"),
    "users_logout": reverse("users:logout"),
    "users_signup": reverse("users:signup"),
}


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.not_author = User.objects.create(username='Not author')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title="Заголовок",
            text="Текст",
            author=cls.author,
        )
        cls.detail_url = URLS["notes_detail"](cls.note.slug)
        cls.edit_url = URLS["notes_edit"](cls.note.slug)
        cls.delete_url = URLS["notes_delete"](cls.note.slug)
        cls.home_url = URLS["notes_home"]
        cls.login_url = URLS["users_login"]
        cls.logout_url = URLS["users_logout"]
        cls.signup_url = URLS["users_signup"]
        cls.notes_list_url = URLS["notes_list"]
        cls.add_url = URLS["notes_add"]
        cls.success_url = URLS["notes_success"]
        cls.data = {
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": "new-slug"
        }
