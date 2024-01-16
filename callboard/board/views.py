from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, OneTimeCode
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
import random


def generate_one_time_code():
    return ''.join(random.choice('abcdef') for _ in range(6))


def send_one_time_code_email(email, code):
    subject = 'Код подтверждения регистрации'
    message = f'Ваш код подтверждения: {code}'
    from_email = 'noreply@example.com'
    send_mail(subject, message, from_email, [email])


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'postlist.html'
    context_object_name = 'postlist'
    paginate_by = 10


class Postdetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('post.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            one_time_code = generate_one_time_code()
            OneTimeCode.objects.create(code = one_time_code, user = user)
            send_one_time_code_email(user.email, one_time_code)
            user = authenticate(request, username = form.cleaned_data['username'],
                                password = form.cleaned_data['password1'])
            login(request, user)

            return redirect('post_list')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
