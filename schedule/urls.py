from django.conf.urls import url

from . import views

app_name = 'schedule'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ajax
    url(r'^ajax/display_user_type', views.display_user_type, name='display_user_type'),

    url(r'^add_schedule$', views.create_schedule, name='add-schedule')

]