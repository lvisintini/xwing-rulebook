from rule.views import rulebook


def index(request, *args, **kwargs):
    return rulebook(request, *args, **kwargs)
