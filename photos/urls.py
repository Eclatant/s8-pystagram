from django.conf.urls import url

from . import views


app_name = 'photos'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.view_post, name='view'),
    url(r'^$', views.list_posts, name='list'),
]

