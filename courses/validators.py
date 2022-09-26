from django import forms


class BasicForm(forms.Form):
    name = forms.CharField(min_length=10, max_length=100)
    description = forms.CharField(min_length=10, max_length=100)
