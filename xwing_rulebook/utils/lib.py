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
        return [content, ]
    else:
        chunk = content[:length+1].rsplit(' ', maxsplit=1)[0]
        reminder = content[len(chunk)+1:]
        res = [chunk, ]
        res.extend(word_sensitive_grouper(reminder, length))
        return res
