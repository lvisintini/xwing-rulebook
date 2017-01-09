from rule.views import single_page_rulebook


def index(request, *args, **kwargs):
    return single_page_rulebook(request, *args, **kwargs)
