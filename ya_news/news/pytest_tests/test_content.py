from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from news.forms import CommentForm
from news.models import News, Comment

User = get_user_model()


@pytest.mark.django_db
def test_news_count(client):
    """
    Проверка количества новостей на главной странице.
    Количество новостей не должно превышать NEWS_COUNT_ON_HOME_PAGE.
    """
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    """
    Проверка порядка новостей на главной странице.
    Новости должны быть отсортированы от самой свежей к самой старой.
    """
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client):
    """
    Проверка порядка комментариев на странице новости.
    Комментарии должны быть отсортированы в хронологическом порядке.
    """
    news = News.objects.create(title='Тестовая новость', text='Просто текст.')
    detail_url = reverse('news:detail', args=(news.id,))
    response = client.get(detail_url)
    assert response.status_code == 200
    author = User.objects.create(username='Комментатор')
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client):
    """
    Проверка доступности формы для анонимного пользователя.
    Анонимному пользователю форма для отправки комментария недоступна.
    """
    news = News.objects.create(title='Тестовая новость', text='Просто текст.')
    detail_url = reverse('news:detail', args=(news.id,))
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(client):
    """
    Проверка доступности формы для авторизованного пользователя.
    Авторизованному пользователю форма для отправки комментария доступна.
    """
    news = News.objects.create(title='Тестовая новость', text='Просто текст.')
    detail_url = reverse('news:detail', args=(news.id,))
    author = User.objects.create(username='Комментатор')
    client.force_login(author)
    response = client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
