from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from .constants import HTTP_NOT_FOUND
from conftest import TEXT_COMMENT, NEW_TEXT_COMMENT


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    """Анонимный пользователь не может отправить комментарий."""
    expected_comment_count = Comment.objects.count()
    client.post(news_detail_url, data=NEW_TEXT_COMMENT)
    comments_count = Comment.objects.count()
    assert comments_count == expected_comment_count


def test_user_can_create_comment(author_client, author, news_detail_url):
    """Авторизованный пользователь может отправить комментарий."""
    author_client.post(news_detail_url, data=NEW_TEXT_COMMENT)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == NEW_TEXT_COMMENT['text']
    assert comment.news.id == int(news_detail_url.split('/')[-2])
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_detail_url):
    """
    Если комментарий содержит запрещённые слова, он не будет
    опубликован, а форма вернёт ошибку.
    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    expected_comment_count = Comment.objects.count()
    comments_count = Comment.objects.count()
    assert comments_count == expected_comment_count


def test_author_can_delete_comment(author_client,
                                   news_detail_url, comment_delete_url
                                   ):
    """Авторизованный пользователь может удалять свои комментарии."""
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, news_detail_url + '#comments')
    expected_comment_count = Comment.objects.count()
    comments_count = Comment.objects.count()
    assert comments_count == expected_comment_count


def test_user_cant_delete_comment_of_another_user(admin_client, 
                                                  comment_delete_url
                                                  ):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    response = admin_client.delete(comment_delete_url)
    assert response.status_code == HTTP_NOT_FOUND
    expected_comment_count = Comment.objects.count()
    comments_count = Comment.objects.count()
    assert comments_count == expected_comment_count


def test_author_can_edit_comment(author_client, news_detail_url, 
                                 comment_edit_url, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(comment_edit_url, data=NEW_TEXT_COMMENT)
    assertRedirects(response, news_detail_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_TEXT_COMMENT['text']


def test_user_cant_edit_comment_of_another_user(admin_client, comment,
                                                comment_edit_url):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(comment_edit_url, data=NEW_TEXT_COMMENT)
    assert response.status_code == HTTP_NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == TEXT_COMMENT
