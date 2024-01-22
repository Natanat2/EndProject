from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length = 32, unique = True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    postAuthor = models.ForeignKey(User, on_delete = models.CASCADE)
    postCategory = models.ForeignKey(Category, on_delete = models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 128, null = False)
    content = RichTextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args = [str(self.id)])


class Response(models.Model):
    responsePost = models.ForeignKey(Post, on_delete = models.CASCADE)
    responseUser = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    approve = models.BooleanField(default = False)


class OneTimeCode(models.Model):
    code = models.CharField(max_length = 6)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.code}"


class Subscription(models.Model):
    user = models.ForeignKey(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'subscriptions',
    )
    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name = 'subscriptions',
    )
