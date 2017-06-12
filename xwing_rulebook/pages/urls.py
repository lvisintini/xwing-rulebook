from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^styleguide$', views.styleguide, name='styleguide'),
]
