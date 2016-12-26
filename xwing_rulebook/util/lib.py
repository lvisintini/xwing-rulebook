from django.template import Context, loader


def render_template(template, context):
    t = loader.get_template(template)
    c = Context(context)
    return t.render(c)
