from rules.views import rules_index
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def index(request, *args, **kwargs):
    return rules_index(request, *args, **kwargs)


@staff_member_required
def styleguide(request):
    return render(request, 'styleguide.html', {})
