import tinymce.models
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length = 32, unique = True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    postAuthor = models.ForeignKey(User, on_delete = models.CASCADE)
    postCategory = models.ForeignKey(Category, on_delete = models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 128, null = False)
    text = tinymce.models.HTMLField()

    def __str__(self):
        return self.title


class Response(models.Model):
    responsePost = models.ForeignKey(Post, on_delete = models.CASCADE)
    responseUser = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    approve = models.BooleanField(default = False)
