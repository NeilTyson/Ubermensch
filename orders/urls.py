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

    # billing statements
    url(r'billing_statement/(?P<order_id>[0-9]+)/(?P<percentage>[0-9]+)/(?P<code>[0-9])/(?P<template_no>[0-9])$',
        views.generate_billing_statement, name='generate-bs'),
    url(r'view_billing_statements/(?P<order_id>[0-9]+)$', views.billing_statement_lists, name='bs-list'),
    url(r'view_billing_statement/(?P<id>[0-9]+)$', views.view_billing_statement, name='view-bs'),

    # official receipts
    url(r'official_receipt/(?P<order_id>[0-9]+)/(?P<percentage>[0-9]+)/(?P<template_no>[0-9]+)$',
        views.generate_official_receipt, name='generate-or'),
    url(r'view_official_receipts/(?P<order_id>[0-9]+)$', views.official_receipt_list, name='or-list'),
    url(r'view_official_receipt/(?P<id>[0-9]+)$', views.view_official_receipt, name='view-or'),

    # all schedules
    url(r'schedule_engineers/(?P<order_id>[0-9]+)$', views.schedule_engineers, name='schedule_engineers'),
    url(r'schedule_delivery/(?P<order_id>[0-9]+)$', views.schedule_delivery, name='schedule-delivery'),

    # delivery receipts
    url(r'delivery_receipt/(?P<order_id>[0-9]+)/(?P<template_no>[0-9]+)$',
        views.generate_delivery_receipt, name='generate-dr'),
    url(r'view_delivery_receipts/(?P<order_id>[0-9]+)$', views.delivery_receipt_list, name='dr-list'),
    url(r'view_delivery_receipt/(?P<id>[0-9]+)$', views.view_delivery_receipt, name='view-dr'),


    url(r'product_retrieval/(?P<order_id>[0-9]+)$', views.product_retrieval_phase, name='product_retrieval'),
    url(r'delivery/(?P<order_id>[0-9]+)$', views.delivery, name='delivery'),
    url(r'installation/(?P<order_id>[0-9]+)$', views.installation, name='installation'),
    url(r'maintenance/(?P<order_id>[0-9]+)$', views.maintenance, name='maintenance'),


    # project
    url(r'installation/project/(?P<order_id>[0-9]+)$', views.view_project, name='view-project'),

    # ajax add order line
    url(r'ajax/add_order_line$', views.add_order_line, name='add-order-line'),
    url(r'ajax/view_engineers$', views.view_engineers, name='view-engineers'),
    url(r'ajax/view_delivery_people$', views.view_delivery_people, name='view-delivery-people'),
]