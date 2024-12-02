from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

from ..forms import PostForm
from ..models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):

    global USERNAME
    USERNAME = 'NoName'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.group = Group.objects.create(
            title = 'Тестовая группа',
            slug = 'test-slug',
            description = 'Тестовое описание',
        )
        cls.post = Post.objects.create(
            author = cls.user,
            text = 'Тестовый пост post',
            group = cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.user = PostCreateFormTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Ввод текста поста',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data = form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': USERNAME}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(text='Ввод текста поста').exists()
        )

    def test_author_edit_post(self):
        """Валидная форма изменяет запись в Posts."""
        form_data = {
            'text': 'Ввод текста поста',
            'group': self.group.pk,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(id=self.group.pk)
        self.authorized_client.get(f'/posts/{self.post.pk}/edit/')
        form_data = {
            'text': 'Изменение текста поста',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        post_edit = Post.objects.get(id=self.group.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(post_edit.text, 'Изменение текста поста')
