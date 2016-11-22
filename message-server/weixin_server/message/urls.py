
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^watch_index/$', views.watch_index, name='watch_index'),
    url(r'^watch_edit/$', views.watch_edit, name='watch_edit'),
    url(r'^task_index/$', views.task_index, name='task_index'),
    url(r'^task_delete/(?P<task_id>\d+)$', views.task_delete, name='task_delete'),
    url(r'^task_create/$', views.task_create, name='task_create'),
    url(r'^task_edit/(?P<task_id>\d+)$', views.task_edit, name='task_edit'),
    url(r'^task_detail/(?P<task_id>\d+)$', views.task_detail, name='task_detail'),
]
