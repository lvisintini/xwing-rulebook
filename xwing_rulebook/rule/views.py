from django.shortcuts import render
from .models import RuleBook


def rulebook(request):
    rb = RuleBook.objects.first()

    context = {
        'rb': rb,
    }

    return render(request, 'html/rulebook.html', context)
