from django import forms
from django.forms import ValidationError

from .models import Post, Comment


class PostForm(forms.ModelForm):
    #    tags = forms.CharField(required=False)
    tagtext = forms.CharField()

    class Meta:
        model = Post
        fields = ('category', 'content',)  # 모든 걸 하고 싶으면 __all__ (?)

#    def clean(self):
#        password1 = self.cleaned_data['password1']
#        password2 = self.cleaned_data['password2']
#        if password1 != password2:
#            self.add_error('password1', '비번이 일치하지 않습니다')

    def clean_content(self):
        content = self.cleaned_data['content']  # 이미 정제된 상황
        if '바보' in content:
            raise ValidationError('금지어가 있습니다.')
        return content


class SimpleForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=10)
    content = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
