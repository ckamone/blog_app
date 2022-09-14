from django import forms

class SearchForm(forms.Form):
    id = forms.CharField(label='Your id', max_length=100)