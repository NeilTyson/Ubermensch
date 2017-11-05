from django.forms import ModelForm
from orders.models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['customer']


class AccreditationForm(ModelForm):

    class Meta:
        model = Order
        # fields = ['vendor_application', 'bir_certificate', 'dole_certification', 'org_chart', 'sec_registration_form',
        #           'sss_certificate']

        # TODO
        # fields = ['vendor_application']
        fields = []




