from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard_page),
    url(r'^trips/(?P<id>\d+)', views.view_trip_page),
    url(r'^trips/new', views.new_trip_page),
    url(r'^action_new_trip', views.action_new_trip),
    url(r'^action_remove_trip/(?P<id>\d+)', views.action_remove_trip),
    url(r'^trips/edit/(?P<id>\d+)', views.edit_trip_page),
    url(r'^action_edit_trip/(?P<id>\d+)', views.action_edit_trip),
    url(r'^trips/join/(?P<id>\d+)', views.action_join_trip),
    url(r'^trips/cancel/(?P<id>\d+)', views.action_cancel),
]
