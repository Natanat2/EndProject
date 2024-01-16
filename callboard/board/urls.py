from django.urls import path, include

from .views import (PostList, Postdetail, PostCreate, PostEdit, PostDelete, registration_view)

urlpatterns = [
    path('board/', PostList.as_view(), name = 'post_list'),
    path('board/<int:pk>', Postdetail.as_view(), name = 'post_detail'),
    path('board/create', PostCreate.as_view(), name = 'post_create'),
    path('board/<int:pk>/edit/', PostEdit.as_view(), name = 'post_update'),
    path('board/<int:pk>/delete/', PostDelete.as_view(), name = 'post_delete'),
    path('register/', registration_view, name='registration_view'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
