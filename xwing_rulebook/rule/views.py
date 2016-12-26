from django.shortcuts import render
from .models import RuleBook


def rulebook(request):
    rl = RuleBook.objects.first()

    context = {
        'rl': rl
    }

    return render(request, 'html/rulebook.html', context)
