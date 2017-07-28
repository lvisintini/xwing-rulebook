from django.conf.urls import url, include
from django.contrib.sitemaps import views as sitemap_views

from . import views
from .sitemaps import sitemaps

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^styleguide$', views.styleguide, name='styleguide'),
    url(r'^resources$', views.resources, name='resources'),
    url(r'^maneuvers$', views.maneuvers, name='maneuvers'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^wall-of-fame', views.wall_of_fame, name='wall-of-fame'),
    url(r'^about', views.about, name='about'),

    url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps, 'sitemap_url_name': 'pages:sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='sitemaps'),

    url(r'^robots\.txt', include('robots.urls')),
    url(r'^manifest\.json', views.manifest, name='manifest.json'),
    url(r'^browserconfig\.xml', views.browser_config, name='browserconfig.xml'),
]
