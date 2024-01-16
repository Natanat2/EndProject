from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'postAuthor',
            'postCategory',
            'title',
            'text',
            'content',
        ]

    content = forms.CharField(widget = CKEditorWidget())


class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(max_length = 6, widget = forms.TextInput(attrs = {'autocomplete': 'off'}))
