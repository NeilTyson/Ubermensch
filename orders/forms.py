from django.forms import ModelForm, forms
from orders.models import Order, Contract


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['customer']


class ContractForm(ModelForm):

    class Meta:
        model = Contract
        fields = ['installation_fee', 'engineering_fee', 'consumables_fee', 'payment_terms',
                  'delivery_terms', 'completion', 'warranty']




