import random
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, ConfirmationCodeForm
from .models import Post, OneTimeCode


def generate_one_time_code():
    return ''.join(random.choice('abcdef') for _ in range(6))


def send_one_time_code_email(email, code, request):
    subject = 'Код подтверждения регистрации'
    message = f'Ваш код подтверждения: {code}'
    confirm_url = request.build_absolute_uri(reverse('confirm_registration'))
    html_message = render_to_string('email_template.html', {'code': code, 'confirm_url': confirm_url})
    from_email = 'natanat2@yandex.ru'
    to_email = [email]
    email = EmailMessage(subject, message, from_email, to_email)
    email.content_subtype = 'html'
    email.send()


def confirm_registration(request):
    if request.method == 'POST':
        form = ConfirmationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            if OneTimeCode.objects.filter(code = entered_code, user = request.user).exists():
                OneTimeCode.objects.filter(code = entered_code, user = request.user).delete()

                user_model = get_user_model()
                user = user_model.objects.get(username = request.user.username)

                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    messages.success(request, 'Регистрация успешно завершена!')
                    return redirect('post_list')
                else:
                    messages.error(request, 'Неверные учетные данные. Пожалуйста, попробуйте еще раз.')
            else:
                messages.error(request, 'Неверный код подтверждения. Пожалуйста, попробуйте еще раз.')
    else:
        form = ConfirmationCodeForm()

    return render(request, 'confirm_registration.html', {'form': form})


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


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['postCategory', 'title', 'content']

    def form_valid(self, form):
        form.instance.postAuthor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')


class PostEdit(LoginRequiredMixin, UpdateView):
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
            send_one_time_code_email(user.email, one_time_code, request)
            user = authenticate(request, username = form.cleaned_data['username'],
                                password = form.cleaned_data['password1'])
            login(request, user)

            return redirect('confirm_registration')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
