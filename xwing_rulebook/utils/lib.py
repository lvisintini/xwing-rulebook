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
