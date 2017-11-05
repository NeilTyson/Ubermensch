from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inventory-order', views.inventory_order, name='inventory-order'),
    url(r'^order/(?P<order_id>[0-9]+)', views.order_details_inventory, name='order-details'),
]