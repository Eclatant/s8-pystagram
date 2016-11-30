from django.conf.urls import url

from . import views


app_name = 'photos'

urlpatterns = [
    url(r'^new/$', views.create_post, name='new'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_post, name='edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_post, name='delete'),
    url(r'^(?P<pk>[0-9]+)/$', views.view_post, name='view'),
    url(r'^$', views.list_posts, name='list'),
    url(r'^comments/(?P<pk>[0-9]+)/delete/$', views.delete_comment, name='delete_comment'),
]

