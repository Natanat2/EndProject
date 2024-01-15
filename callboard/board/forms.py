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
        ]

    text = forms.CharField(widget=CKEditorWidget())
