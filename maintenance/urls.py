from django.conf.urls import url

from maintenance import views

app_name = 'maintenance'

urlpatterns = [

    url(r'^(?P<order_id>[0-9]+)', views.maintenance_overview, name='overview'),
    url(r'maintenance_contract_view/(?P<order_id>[0-9]+)', views.maintenance_contract_view, name='contract-view'),
    url(r'add_maintenance_contract/(?P<order_id>[0-9]+)', views.add_maintenance_contract, name='add-contract'),
    url(r'generate_billing_statement', views.generate_billing_statement, name='generate-bs'),
    url(r'generate_official_receipt', views.generate_official_receipt, name='generate-or'),
    url(r'schedule_maintenance', views.schedule_maintenance, name='schedule-maintenance'),
    url(r'finish_order', views.finish_order, name='finish-order'),
    url(r'renew_contract', views.renew_contract, name='renew-contract'),
    url(r'view_contract', views.view_maintenance_contract, name='view-contract'),

    # TROUBLE TICKETS
    url(r'create_ticket', views.create_ticket, name='create-ticket'),
    url(r'view_ticket', views.ticket_details, name='view-ticket'),
    url(r'schedule_inspection', views.schedule_trouble, name='schedule-trouble'),
    url(r'trouble_billing_statement', views.trouble_billing_statement, name='trouble-bs'),
    url(r'trouble_official_receipt', views.trouble_official_receipt, name='trouble-or'),
    url(r'solve_problem', views.solve_problem, name='solve-problem'),
]