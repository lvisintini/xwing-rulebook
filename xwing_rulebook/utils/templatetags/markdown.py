from django.utils.safestring import mark_safe
from django.template import Library

from markdown import markdown

from integrations.templatetags.xwing_icons import xwing_icons

register = Library()


def md2html(subject):
    return mark_safe(
        xwing_icons(
            markdown(
                subject,
                [
                    "markdown.extensions.attr_list",
                    "markdown.extensions.tables",
                    "markdown.extensions.sane_lists",
                    "superscript"
                ]
            )
        )
    )

register.filter('md2html', md2html)
