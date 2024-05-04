from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.custom.all().prefetch_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        categories = [post.category for post in context['posts']]
        context['categories'] = set(categories)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostFromCategory(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        queryset = Post.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        context['category'] = Category.objects.get(slug=category_slug)
        context['categories'] = Category.objects.all()
        return context
