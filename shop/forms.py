from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "city", "phone"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Adınız"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Soyadınız"}),
            "email": forms.EmailInput(attrs={"placeholder": "ornek@email.com"}),
            "address": forms.TextInput(attrs={"placeholder": "Teslimat adresiniz"}),
            "city": forms.TextInput(attrs={"placeholder": "Şehir"}),
            "phone": forms.TextInput(attrs={"placeholder": "05XX XXX XX XX"}),
        }