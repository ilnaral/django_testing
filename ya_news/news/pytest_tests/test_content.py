from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

from news.forms import CommentForm
from news.models import Comment, News

User = get_user_model()


def test_news_count(client, news_home_url):
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
    response = client.get(news_home_url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home_url):
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
    response = client.get(news_home_url)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news_detail_url):
    """
    Проверка порядка комментариев на странице новости.
    Комментарии должны быть отсортированы в хронологическом порядке.
    """
    response = client.get(news_detail_url)
    assert response.status_code == 200
    all_comments = Comment.objects.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, news_detail_url):
    """
    Проверка доступности формы для анонимного пользователя.
    Анонимному пользователю форма для отправки комментария недоступна.
    """
    response = client.get(news_detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(client, author, news_detail_url):
    """
    Проверка доступности формы для авторизованного пользователя.
    Авторизованному пользователю форма для отправки комментария доступна.
    """
    client.force_login(author)
    response = client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
