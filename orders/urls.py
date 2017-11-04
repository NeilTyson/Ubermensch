from django.conf.urls import url

from orders import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_order$', views.add_order, name='add_order'),
    url(r'^(?P<order_id>[0-9]+)', views.order_details, name='order-details'),
    url(r'^accreditation/(?P<order_id>[0-9]+)$', views.accreditation_phase, name='accreditation'),
    url(r'accreditation/upload_accreditation/(?P<order_id>[0-9]+)$', views.upload_documents, name='upload_accreditation')
]