from django.shortcuts import render
from .models import RuleBook


def rulebook(request):
    context = {
        'rl': RuleBook.objects.first()
    }

    return render(request, 'rulebook.html', context)
