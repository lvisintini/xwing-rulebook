from django.conf.urls import url

from faqs import views

app_name = 'faqs'
urlpatterns = [
    url(r'^$', views.faqs, name='index'),
]
