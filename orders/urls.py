from django.conf.urls import url

from orders import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_order$', views.add_order, name='add_order'),
    url(r'^(?P<order_id>[0-9]+)', views.order_details, name='order-details'),

    # contract
    url(r'contract/inspector_report/(?P<order_id>[0-9]+)$', views.inspector_report,
        name='inspector_report'),
    url(r'contract/view_inspector_report/(?P<order_id>[0-9]+)$', views.view_inspector_report,
        name='view-inspector-report'),
    url(r'contract/(?P<order_id>[0-9]+)$', views.purchase_order_phase, name='contract'),
    url(r'contract/generate/(?P<order_id>[0-9]+)$', views.contract_form, name='contract-form'),
    url(r'contract/view/(?P<order_id>[0-9]+)$', views.view_contract, name='view-contract'),

    url(r'billing_statement/(?P<order_id>[0-9]+)/(?P<percentage>[0-9]+)/(?P<code>[0-9])/(?P<template_no>[0-9])$',
        views.generate_billing_statement, name='generate-bs'),
    url(r'view_billing_statement/(?P<order_id>[0-9]+)/(?P<number>[0-9])$', views.view_billing_statement,
        name='view_bs'),


    url(r'billing_statement/(?P<order_id>[0-9]+)/(?P<phase>[0-9]+)$', views.generate_billing_statement_1, name='bill-1'),
    url(r'billing_statement/view/(?P<order_id>[0-9]+)/(?P<phase>[0-9]+)$', views.view_billing_statement_1,
        name='view_bill-1'),
    url(r'official_receipt/(?P<order_id>[0-9]+)/(?P<phase>[0-9]+)$', views.generate_official_receipt_1,
        name='official-receipt-1'),
    url(r'official_receipt/view/(?P<order_id>[0-9]+)/(?P<phase>[0-9]+)$', views.view_official_receipt, name='view_or-1'),
    url(r'schedule_engineers/(?P<order_id>[0-9]+)$', views.schedule_engineers, name='schedule_engineers'),



    url(r'product_retrieval/(?P<order_id>[0-9]+)$', views.product_retrieval_phase, name='product_retrieval'),
    url(r'delivery/(?P<order_id>[0-9]+)$', views.delivery, name='delivery'),
    url(r'installation/(?P<order_id>[0-9]+)$', views.installation, name='installation'),
    url(r'maintenance/(?P<order_id>[0-9]+)$', views.maintenance, name='maintenance'),

    # ajax add order line
    url(r'ajax/add_order_line$', views.add_order_line, name='add-order-line'),
    url(r'ajax/view_engineers$', views.view_engineers, name='view-engineers')
]