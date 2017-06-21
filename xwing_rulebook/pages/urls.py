from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^styleguide$', views.styleguide, name='styleguide'),
    url(r'^resources', views.help_wanted, name='resources'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^wall-of-fame', views.wall_of_fame, name='wall-of-fame'),
    url(r'^about', views.about, name='about'),
]
