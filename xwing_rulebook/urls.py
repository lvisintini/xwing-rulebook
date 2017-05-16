from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('pages.urls')),
    url(r'^books/', include('books.urls')),
    url(r'^rules/', include('rules.urls')),
    url(r'^faq/', include('faqs.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
