from django.conf.urls import url

from orders import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_order$', views.add_order, name='add_order'),
    url(r'^(?P<order_id>[0-9]+)', views.order_details, name='order-details'),

    # project requirements
    url(r'project_requirements/(?P<order_id>[0-9]+)$', views.project_requirements_phase, name='project_requirements'),
    url(r'project_requirements/inspector_report/(?P<order_id>[0-9]+)$', views.inspector_report,
        name='inspector_report'),
    url(r'project_requirements/view_inspector_report/(?P<order_id>[0-9]+)$', views.view_inspector_report,
        name='view-inspector-report'),

    # contract
    url(r'contract/(?P<order_id>[0-9]+)$', views.purchase_order_phase, name='contract'),
    url(r'contract/generate/(?P<order_id>[0-9]+)$', views.contract_form, name='contract-form'),

    url(r'product_retrieval/(?P<order_id>[0-9]+)$', views.product_retrieval_phase, name='product_retrieval'),
    url(r'delivery/(?P<order_id>[0-9]+)$', views.delivery, name='delivery'),
    url(r'installation/(?P<order_id>[0-9]+)$', views.installation, name='installation'),
    url(r'maintenance/(?P<order_id>[0-9]+)$', views.maintenance, name='maintenance'),

    # ajax add order line
    url(r'ajax/add_order_line$', views.add_order_line, name='add-order-line')
]