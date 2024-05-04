from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import Post


class PostViewMiddleware:
    """
    Middleware для увеличения счетчика просмотров постов блога.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'slug' in view_kwargs:
            self.increment_views(view_kwargs['slug'], request.session.session_key)

    @staticmethod
    def increment_views(slug, session_key):
        cache_key = f'post_views:{slug}:{session_key}'
        if not cache.get(cache_key):
            try:
                post = Post.objects.get(slug=slug)
                post.views += 1
                post.save(update_fields=['views'])
                cache.set(cache_key, True)
            except Post.DoesNotExist:
                pass
