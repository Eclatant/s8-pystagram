from django import forms
from django.forms import ValidationError

from .models import Post
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )


class PostForm(forms.ModelForm):
    tagtext = forms.CharField()

    class Meta:
        model = Post
        fields = ('category', 'content', )

#    def clean(self):
#        password1 = self.cleaned_data['password1']
#        password2 = self.cleaned_data['password2']
#        if password1 != password2:
#            self.add_error('password1', '비번이 일치하지 않음')

    def clean_content(self):
        content = self.cleaned_data['content']
        if '바보' in content:
            raise ValidationError('금지어가 있습니다')
        return content


class SimpleForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=10)
    content = forms.CharField(widget=forms.Textarea)

