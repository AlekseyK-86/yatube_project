from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField('Текст поста', help_text='Введите текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name = 'posts', 
        verbose_name='Автор', 
        )
    group = models.ForeignKey(
        Group, 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        verbose_name='Группа', 
        help_text='Группа, к которой будет относиться пост'
        )
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return self.text[:15]
