from django.conf.urls import url
from django.contrib import admin

from photos.views import list_posts
from photos.views import view_post


urlpatterns = [
    url(r'^photos/(?P<pk>[0-9]+)/$', view_post, name='view'),
    url(r'^photos/$', list_posts, name='list'),
    url(r'^admin/', admin.site.urls),
]
