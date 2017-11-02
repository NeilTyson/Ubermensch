from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_product$', views.create_product, name='add-product'),
    url(r'^suppliers$', views.suppliers, name='suppliers'),
    url(r'^suppliers/add$', views.add_supplier, name='add-supplier'),
    url(r'^categories$', views.category_view, name='categories'),
    url(r'^categories/add$', views.add_category, name='add-category')
]