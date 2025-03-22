from http import HTTPStatus

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from news.models import Comment, News

User = get_user_model()


@pytest.mark.django_db
def test_pages_availability(client):
    """
    Проверка доступности публичных страниц.
    Тестирует доступность главной страницы, страницы новости,
    страниц регистрации, входа и выхода из системы.
    """
    news = News.objects.create(title='Заголовок', text='Текст')
    urls = (
        ('news:home', None),
        ('news:detail', (news.id,)),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
    for name, args in urls:
        url = reverse(name, args=args)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_redirect_for_anonymous_client(client):
    """
    Проверка редиректа для неавторизованных пользователей.
    Проверяет, что неавторизованные пользователи перенаправляются
    на страницу логина
    при попытке доступа к страницам редактирования или удаления комментариев.
    """
    news = News.objects.create(title='Заголовок', text='Текст')
    author = User.objects.create(username='Автор')
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    login_url = reverse('users:login')
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        redirect_url = f'{login_url}?next={url}'
        response = client.get(url)
        assert response.url == redirect_url


@pytest.mark.django_db
def test_edit_delete_pages_availability_for_author(client):
    """
    Проверка доступа автора к страницам редактирования и удаления.
    Тестирует, что автор комментария может доступиться к страницам
    редактирования и удаления своего комментария.
    """
    news = News.objects.create(title='Заголовок', text='Текст')
    author = User.objects.create(username='Автор')
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    client.force_login(author)
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_edit_delete_pages_unavailability_for_another_user(client):
    """
    Проверка недоступности страниц редактирования и
    удаления для других пользователей.
    Тестирует, что другие пользователи получают ошибку 404 при попытке доступа
    к страницам редактирования или удаления чужого комментария.
    """
    news = News.objects.create(title='Заголовок', text='Текст')
    author = User.objects.create(username='Автор')
    reader = User.objects.create(username='Читатель')
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    client.force_login(reader)
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
