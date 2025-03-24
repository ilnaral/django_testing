import pytest

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


User = get_user_model()

TEXT_COMMENT = 'Текст комментария'
NEW_TEXT_COMMENT = {'text': 'Новый текст'}


@pytest.fixture
def new_text_comment():
    return {'text': 'Новый текст'}


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Блатной')


@pytest.fixture
def author_client(author, client):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.today(),
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text=TEXT_COMMENT,
        news=news,
        author=author
    )
    return comment


@pytest.fixture
def list_news():
    today, list_news = datetime.today(), []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        news = News.objects.create(
            title='Новость {index}',
            text='Текст новости',
        )
        news.date = today - timedelta(days=index)
        news.save()
        list_news.append(news)
    return list_news


@pytest.fixture
def list_comments(news, author):
    now, list_comment = timezone.now(), []
    for index in range(2):
        comment = Comment.objects.create(
            text='Текст {index}',
            news=news,
            author=author,
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        list_comment.append(comment)


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
