from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.template import Context, loader
from itertools import zip_longest


def render_template(template, context):
    t = loader.get_template(template)
    c = Context(context)
    return t.render(c)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def word_sensitive_grouper(content, length=100):
    if len(content) <= length:
        if content == '':
            return []
        return [content, ]
    else:
        if ' ' in content[:length+1]:
            chunk = content[:length+1].rsplit(' ', maxsplit=1)[0]
        else:
            # This is in case a word is longer than the provided length
            chunk = content.split(' ', maxsplit=1)[0]
        reminder = content[len(chunk)+1:]
        res = [chunk, ]
        res.extend(word_sensitive_grouper(reminder, length))
        return res


def list_url_names(urlpatterns, namespaces=None):
    if namespaces is None:
        namespaces = []

    for pattern in urlpatterns:
        if isinstance(pattern, RegexURLResolver):
            for view_name in list_url_names(pattern.url_patterns, namespaces=namespaces + [pattern.namespace, ]):
                yield view_name
        elif isinstance(pattern, RegexURLPattern):

            if not hasattr(pattern.callback, '__name__'):
                # A class-based view
                view_path = pattern.callback.__class__.__module__ + '.' + pattern.callback.__class__.__name__
            else:
                # A function-based view
                view_path = pattern.callback.__module__ + '.' + pattern.callback.__name__

            view_path = pattern.name or view_path

            yield ':'.join([x for x in namespaces if x] + [view_path, ])


def site_url_from_request(request):
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    return '{}://{}'.format(protocol, domain)