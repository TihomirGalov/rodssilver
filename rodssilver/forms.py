from django import forms
from orders.models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'