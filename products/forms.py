from django import forms

from products.models import Product, Supplier, Category


class ProductForm(forms.ModelForm):

    supplier = forms.ModelMultipleChoiceField(Supplier.objects.all(), required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'unit', 'unit_cost',
                  'category', 'supplier']

        widgets = {
            'description': forms.Textarea
        }


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person_first_name', 'contact_person_last_name', 'e_mail', 'contact_no']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'description': forms.Textarea
        }