from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inventory-order', views.inventory_order, name='inventory-order'),
    url(r'^order/(?P<order_id>[0-9]+)', views.order_details_inventory, name='order-details'),
    url(r'^request-inventory', views.request_inventory, name='request-inventory'),
    url(r'^view-po/(?P<po_id>[0-9]+)', views.view_po, name='view-po'),
    url(r'^view-all-po', views.view_all_po, name='view-all-po'),
    url(r'^confirm-product-retrieval(?P<po_id>[0-9]+)', views.confirm_product_retrieval, name='confirm-product-retrieval'),
    url(r'^ajax/get_products_using_supplier', views.get_products_using_supplier, name='get_products_using_supplier'),
    url(r'^ajax/generate_po', views.generate_po, name='generate_po'),

    url(r'request_supplies', views.request_products, name='request-supplies')
]