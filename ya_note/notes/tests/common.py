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
        cls.author = User.objects.create(username="author")
        cls.auth_user = User.objects.create(username="auth_user")
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.auth_user_client = Client()
        cls.auth_user_client.force_login(cls.auth_user)
        cls.note = Note.objects.create(
            title="Заголовок",
            text="Текст",
            author=cls.author,
        )
        cls.data = {
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": "new-slug"
        }