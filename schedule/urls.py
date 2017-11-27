from django.conf.urls import url

from . import views

app_name = 'schedule'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ajax
    url(r'^ajax/display_user_type', views.display_user_type, name='display_user_type'),
    url(r'^ajax/display_events', views.display_events, name='display_events'),
    url(r'^ajax/display_own_events', views.display_own_events, name='display_events'),
    url(r'^ajax/view_people', views.view_involved_people, name='view_people'),

    url(r'^add_schedule$', views.create_schedule, name='add-schedule'),
    url(r'^details/(?P<pk>[0-9]+)$', views.details, name='details'),
    url(r'my_schedule$', views.my_schedule, name='my-schedule'),
    url(r'mark_complete/(?P<schedule_id>[0-9]+)$', views.mark_as_complete, name='complete'),
]