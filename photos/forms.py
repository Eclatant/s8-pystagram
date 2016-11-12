from django import forms

from .models import Post


class PostForm(forms.ModelForm):
#    content = forms.IntegerField()

    class Meta:
        model = Post
        fields = ('category', 'content', 'tags', )


class SimpleForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=10)
    content = forms.CharField(widget=forms.Textarea)

