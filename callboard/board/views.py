import random
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef

from .forms import PostForm, ConfirmationCodeForm, ResponseForm
from .models import Post, OneTimeCode, Category, Subscription, Response
from .signals import send_notification_email


def generate_one_time_code():
    return ''.join(random.choice('abcdef') for _ in range(6))


def send_one_time_code_email(email, code, request):
    subject = 'Код подтверждения регистрации'
    message = f'Ваш код подтверждения: {code}'
    confirm_url = request.build_absolute_uri(reverse('confirm_registration'))
    html_message = render_to_string('email_template.html', {'code': code, 'confirm_url': confirm_url})
    from_email = 'natanat2@yandex.ru'

    send_mail(
        subject,
        message,
        from_email,
        [email],
        html_message = html_message,
        fail_silently = False,
    )


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
            messages.error(request, 'Пожалуйста, введите корректный код.')
    else:
        form = ConfirmationCodeForm()

    return render(request, 'confirm_registration.html', {'form': form})


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


@login_required
def add_response_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit = False)
            response.responsePost = post
            response.responseUser = request.user
            response.approve = None
            response.save()
            messages.success(request, 'Отклик добавлен!')
            return redirect('post_detail', pk = post.pk)
    else:
        form = ResponseForm()

    return render(request, 'add_response_to_post.html', {'form': form, 'post': post})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id = category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user = request.user, category = category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user = request.user, category = category, ).delete()

    categories_with_subsriptions = Category.objects.annotate(
        user_subscribed = Exists(
            Subscription.objects.filter(
                user = request.user,
                category = OuterRef('pk')
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subsriptions},
    )


@login_required
def private_user_page(request):
    user_posts = Post.objects.filter(postAuthor = request.user)
    responses = Response.objects.filter(responsePost__in = user_posts)
    return render(request, 'private_user_page.html', {'user_posts': user_posts, 'responses': responses})


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


class DeleteResponse(DeleteView):
    model = Response
    template_name = 'delete_response.html'
    success_url = reverse_lazy('private_user_page')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ApproveResponse(UpdateView):
    model = Response
    template_name = 'approve_response.html'
    fields = ['approve']

    def form_valid(self, form):
        response = form.save(commit=False)
        response.approve = True
        response.save()
        messages.success(self.request, 'Отклик принят!')
        mail_subject = 'Ваш отклик принят'
        message = f'Ваш отклик на пост "{response.responsePost}" был принят.'
        to_email = response.responseUser.email
        send_notification_email(mail_subject, message, to_email)
        return redirect('private_user_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при принятии отклика.')
        return redirect('private_user_page')
