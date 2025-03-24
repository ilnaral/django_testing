from .constants import HTTP_OK, get_login_redirect_url


def test_pages_status(client, news_home_url, news_detail_url, login_url,
                      logout_url, signup_url):
    urls = (
        news_home_url,
        news_detail_url,
        login_url,
        logout_url,
        signup_url,
    )
    for url in urls:
        response = client.get(url)
        assert response.status_code == HTTP_OK


def test_redirects(client, comment_delete_url, comment_edit_url, login_url):
    for url in (comment_delete_url, comment_edit_url):
        redirect_url = get_login_redirect_url(url, login_url)
        response = client.get(url)
        assert response.url == redirect_url
