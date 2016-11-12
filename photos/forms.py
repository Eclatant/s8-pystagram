from django import forms


class SimpleForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=10)
    content = forms.CharField(widget=forms.Textarea)

