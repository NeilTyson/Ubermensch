from django.conf.urls import url

from orders import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_order$', views.add_order, name='add_order'),
    url(r'^(?P<order_id>[0-9]+)', views.order_details, name='order-details'),
    url(r'project_requirements/(?P<order_id>[0-9]+)$', views.project_requirements_phase, name='project_requirements'),
    url(r'project_requirements/inspector_report/(?P<order_id>[0-9]+)$', views.inspector_report,
        name='inspector_report'),
    url(r'contract/(?P<order_id>[0-9]+)$', views.purchase_order_phase, name='contract'),
    url(r'product_retrieval/(?P<order_id>[0-9]+)$', views.product_retrieval_phase, name='product_retrieval'),
    url(r'delivery/(?P<order_id>[0-9]+)$', views.delivery, name='delivery'),
    url(r'installation/(?P<order_id>[0-9]+)$', views.installation, name='installation'),
    url(r'maintenance/(?P<order_id>[0-9]+)$', views.maintenance, name='maintenance'),
]