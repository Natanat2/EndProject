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
            'content',
        ]

    widgets = {
        'content': CKEditorWidget(),
    }

    content = forms.CharField(widget=CKEditorWidget(), required=False)

class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(max_length = 6, widget = forms.TextInput(attrs = {'autocomplete': 'off'}))
