from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def news():
    """Фикстура новости"""
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def id_for_news(news):
    """Фикстура id новости"""
    return news.id,


@pytest.fixture
def author(django_user_model):
    """Автор"""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    """Залогиненный автор"""
    client.force_login(author)
    return client


@pytest.fixture
def comment(author, news):
    """Комментик"""
    comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария'
    )
    return comment


@pytest.fixture
def all_news():
    """набор новостей"""
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def detail_url(id_for_news):
    """урл для проверки комментика"""
    return reverse('news:detail', args=id_for_news)


@pytest.fixture
def news_with_comment(news, author):
    """набор комментиков"""
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comment


@pytest.fixture
def form_data_comment():
    """форм дата комментика"""
    COMMENT_TEXT = 'Текст комментария'
    return {'text': COMMENT_TEXT}


@pytest.fixture
def reader(django_user_model):
    """Читатель"""
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader, client):
    """Залогиненный читатель"""
    client.force_login(reader)
    return client


@pytest.fixture
def id_for_comment(comment):
    """Фикстура id комментика"""
    return comment.id,


@pytest.fixture
def edit_url(id_for_comment):
    """Урл для редактирования комментика"""
    return reverse('news:edit', args=id_for_comment)


@pytest.fixture
def delete_url(id_for_comment):
    """Урл для удаления комментика"""
    return reverse('news:delete', args=id_for_comment)


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def form_data_new_comment():
    """форм дата нового комментика"""
    NEW_COMMENT_TEXT = 'Обновлённый комментарий'
    return {'text': NEW_COMMENT_TEXT}
