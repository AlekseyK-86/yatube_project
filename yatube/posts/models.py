from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Group(models.Model):
    title = models.TextField('Название группы')
    slug = models.TextField('Адрес')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title  


class Post(models.Model):
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name = 'posts'
        )
    group = models.ForeignKey(
        Group, 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE
        )
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return self.text
 