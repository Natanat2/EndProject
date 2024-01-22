from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from .views import (PostList, Postdetail, PostCreate, PostEdit, PostDelete, registration_view, confirm_registration,
                    subscriptions, add_response_to_post)

urlpatterns = [
    path('board/', PostList.as_view(), name = 'post_list'),
    path('board/<int:pk>', Postdetail.as_view(), name = 'post_detail'),
    path('board/create', PostCreate.as_view(), name = 'post_create'),
    path('board/<int:pk>/edit/', PostEdit.as_view(), name = 'post_update'),
    path('board/<int:pk>/delete/', PostDelete.as_view(), name = 'post_delete'),
    path('register/', registration_view, name = 'registration_view'),
    path('confirm-registration/', confirm_registration, name = 'confirm_registration'),
    path('login/', LoginView.as_view(next_page = 'post_list'), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = 'post_list'), name = 'logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('subscriptions/', subscriptions, name = 'subscriptions'),
    path('post/<int:pk>/add_response/', add_response_to_post, name = 'add_response_to_post'),
]
