from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


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
    template_name ='post_delete.html'
    success_url = reverse_lazy('post_list')

