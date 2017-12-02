from django.conf.urls import url

from maintenance import views

app_name = 'maintenance'

urlpatterns = [

    url(r'^(?P<order_id>[0-9]+)', views.maintenance_overview, name='overview'),
    url(r'maintenance_contract_view/(?P<order_id>[0-9]+)', views.maintenance_contract_view, name='contract-view'),
    url(r'add_maintenance_contract/(?P<order_id>[0-9]+)', views.add_maintenance_contract, name='add-contract'),
    url(r'generate_billing_statement', views.generate_billing_statement, name='generate-bs'),
]