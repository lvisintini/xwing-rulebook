from books.views import single_page_book


def index(request, *args, **kwargs):
    return single_page_book(request, *args, **kwargs)
