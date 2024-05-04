from django.urls import path
from apps.blog.views import PostListView, PostDetailView, PostFromCategory

urlpatterns = [
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<str:slug>/', PostFromCategory.as_view(), name="post_by_category"),
]
