from django.conf.urls import url

from . import views
#from .views import list_posts
#from .views import view_post

app_name = 'photos'    # photos.view 및 photos.list 로 아래가 변경된다

urlpatterns = [
    url(r'^new/$', views.create_post, name='new'),
    url(r'^(?P<pk>[0-9]+)/$', views.view_post, name='view'),
    url(r'^$', views.list_posts, name='list'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_post, name='edit'),
]