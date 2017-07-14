from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static

from integrations.models import Ship
from rules.views import rules_index
from rules.models import Source


def index(request, *args, **kwargs):
    return rules_index(request, *args, **kwargs)


@staff_member_required
def styleguide(request):
    return render(request, 'styleguide.html', {})


def help_wanted(request):
    sources = Source.enriched.all()

    return render(request, 'resources.html', {
        'sources': sources
    })


def contact(request):
    return render(request, 'contact.html', {})


def wall_of_fame(request):
    return render(request, 'wall_of_fame.html', {})


def about(request):
    return render(request, 'about.html', {})


def manifest(request):
    data = {
        "name": "XWing Rulebook",
        "icons": [
            {
                "src": static("favicons/android-chrome-192x192.png"),
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": static("favicons/android-chrome-512x512.png"),
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#3892a6",
        "background_color": "#3892a6",
        "display": "standalone"
    }

    return JsonResponse(data)


def manuevers(request):
    ships = Ship.objects.all()
    return render(request, 'maneuvers.html', {'ships': ships})


def browser_config(request):
    data = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<browserconfig>'
        '    <msapplication>'
        '        <tile>'
        '            <square150x150logo src="{}"/>'
        '            <TileColor>#3892a6</TileColor>'
        '        </tile>'
        '    </msapplication>'
        '</browserconfig>'
    ).format(static("favicons/mstile-150x150.png"))

    return HttpResponse(data, content_type='application/xml')
