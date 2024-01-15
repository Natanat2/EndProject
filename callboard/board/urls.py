from django.urls import path

from .views import (PostList, Postdetail, PostCreate, PostEdit, PostDelete)


urlpatterns = [
   path('board/', PostList.as_view(), name='post_list'),
   path('board/<int:pk>', Postdetail.as_view(), name='post_detail'),
   path('board/create', PostCreate.as_view(), name='post_create'),
   path('board/<int:pk>/edit/', PostEdit.as_view(), name='post_update'),
   path('board/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]