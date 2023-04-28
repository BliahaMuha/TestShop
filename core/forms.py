from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(max_length=200, label='Адрес')
