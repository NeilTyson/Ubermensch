from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.home, name='index'),
    # url(r'^register$', views.ProfileFormView.as_view(), name='register'),
    url(r'^login$', views.SignInView.as_view(), name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^customers$', views.customer_index, name='customers-index'),
    url(r'^customers/add_customer$', views.add_customer, name='add-customer')
]