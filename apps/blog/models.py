from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from apps.services.utils import unique_slugify


class PostManager(models.Manager):
    """
    Кастомный менеджер для модели постов
    """

    def get_queryset(self):
        """
        Список постов (SQL запрос с фильтрацией по статусу опубликованно)
        """
        return super().get_queryset().select_related('author').filter(status='published')


class Post(models.Model):
    """
    Модель постов блога
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликована'),
        ('draft', 'Черновик'),
        ('archive', 'Архив'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')

    title = models.CharField(max_length=70, verbose_name='Заголовок')
    content = models.TextField(max_length=500, verbose_name='Описание')
    thumbnail = models.ImageField(default='post_default.png',
                                  upload_to='images/thumbnails/%d-%m-%Y/',
                                  blank=True,
                                  verbose_name='Изображение',
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
                                  )
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='URL поста')
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус записи', max_length=10)
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name='Просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    objects = models.Manager()
    custom = PostManager()

    class Meta:
        ordering = ['-created_at', '-views']
        indexes = [models.Index(fields=['-created_at', 'status', 'views'])]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        При сохранении и отсутствии слага, генерируем и проверяем на уникальность
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)

        super().save(*args, **kwargs)


class Category(models.Model):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('post_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title
