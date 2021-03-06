from django.conf.urls import url

from rules import views

app_name = 'rules'
urlpatterns = [
    url(r'^$', views.rules_index, name='index'),
    url(r'^(?P<rule_slug>[\w-]+)/$', views.rule, name='rule'),
]
