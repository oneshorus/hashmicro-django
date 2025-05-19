from django import forms
from .models import Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'price', 'stock']


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    barcode = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    stock = forms.IntegerField()

    def from_instance(self, instance):
        self.initial = {
            'name': instance.name,
            'barcode': instance.barcode,
            'price': instance.price,
            'stock': instance.stock,
        }

    def update_instance(self, instance):
        instance.name = self.cleaned_data['name']
        instance.barcode = self.cleaned_data['barcode']
        instance.price = self.cleaned_data['price']
        instance.stock = self.cleaned_data['stock']
        instance.save()
        return instance