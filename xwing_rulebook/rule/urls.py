from django.conf.urls import url

from . import views

app_name = 'rule'
urlpatterns = [
    url(r'^(?P<rulebook_slug>[\w-]+)/$', views.rulebook, name='book'),
    url(r'^(?P<rulebook_slug>[\w-]+)/(?P<section_slug>[\w-]+)/$', views.rulebook, name='section'),
    url(r'^(?P<rulebook_slug>[\w-]+)/(?P<section_slug>[\w-]+)/(?P<rule_slug>[\w-]+)/$', views.rulebook, name='rule'),
]
