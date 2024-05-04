from django.test import TestCase
from .models import Post


class PostModelTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Это тестовый пост для проверки модели',
            status='published'
        )

    def test_post_creation(self):
        """
        Тестирование создания поста.
        """
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.content, 'Это тестовый пост для проверки модели')
        self.assertEqual(self.post.status, 'published')

    def test_get_absolute_url(self):
        """
        Тестирование метода get_absolute_url.
        """
        expected_url = f'/post/{self.post.slug}/'
        self.assertEqual(self.post.get_absolute_url(), expected_url)
