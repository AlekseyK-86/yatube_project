from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title = 'Тестовая группа',
            slug = 'Тестовый слаг',
            description = 'Тестовое описание',
        )
        cls.post = Post.objects.create(
            author = cls.user,
            text = 'Тестовый пост post',
        )
    
    def test_models_post_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        post = PostModelTest.post
        except_object_name = post.text[:15]
        self.assertEqual(except_object_name, str(post))
    
    def test_models_group_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        group = PostModelTest.group
        except_object_name = group.title
        self.assertEqual(except_object_name, str(group))

    def test_post_title_label(self):
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста')
    
    def test_group_help_text(self):
        post = PostModelTest.post
        verbose = post._meta.get_field('group').help_text
        self.assertEqual(verbose, 'Группа, к которой будет относиться пост')
