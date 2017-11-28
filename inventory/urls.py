from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inventory-order', views.inventory_order, name='inventory-order'),
    url(r'^order/(?P<order_id>[0-9]+)', views.order_details_inventory, name='order-details'),
    url(r'^request-inventory', views.request_inventory, name='request-inventory'),

    url(r'^ajax/get_products_using_supplier', views.get_products_using_supplier, name='get_products_using_supplier'),
]