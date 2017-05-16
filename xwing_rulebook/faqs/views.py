from django.shortcuts import render
from markdowns.faq import FaqsToMarkdown


def faqs(request):
    helper = FaqsToMarkdown(
        anchored=True,
        linked=True,
        anchored_links=True,
        header_level=2,
    )

    context = {
        'faqs2markdown': helper
    }
    return render(request, 'faqs.html', context)
