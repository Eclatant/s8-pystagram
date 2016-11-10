from django.conf.urls import url
from django.contrib import admin

from photos.views import list_posts


urlpatterns = [
    url(r'^photos/$', list_posts, name='list'),
    url(r'^admin/', admin.site.urls),
]
