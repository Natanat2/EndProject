from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length = 32, unique = True)


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete = models.CASCADE)
    postCategory = models.ForeignKey(Category, on_delete = models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 128, null = False)
    text = models.TextField()


    def __str__(self):
        return self.name.title()


class Response(models.Model):
    responsePost = models.ForeignKey(Post, on_delete = models.CASCADE)
    responseUser = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    approve = models.BooleanField(default = False)
