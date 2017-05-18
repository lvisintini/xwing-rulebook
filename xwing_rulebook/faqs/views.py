from django.shortcuts import render
from markdowns.faq import Faqs2Markdown


def faqs(request):
    helper = Faqs2Markdown(
        anchored=True,
        linked=True,
        anchored_links=True,
        header_level=2,
    )

    context = {
        'faqs2markdown': helper
    }
    return render(request, 'faqs.html', context)
