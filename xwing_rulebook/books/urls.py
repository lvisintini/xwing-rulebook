from django.conf.urls import url

from books import views

app_name = 'books'
urlpatterns = [
    url(
        r'^(?:(?P<book_slug>[\w-]+)/)?(?:(?P<section_slug>[\w-]+)/)?(?:(?P<rule_slug>[\w-]+)/)?$',
        views.book, name='book'
    ),
    url(r'^single-page(?:/(?P<book_slug>[\w-]+)/)?$', views.single_page_book, name='single-page-book'),
]
