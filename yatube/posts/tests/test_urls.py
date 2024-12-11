from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from yatube.posts.constants import USERNAME
from yatube.posts.models import Post, Group


User = get_user_model()


class PostURLTests(TestCase):
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

    def setUp(self):
        self.guest_client = Client()
        self.user = PostURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_exists_anonymous(self):
        """Проверка доступности url-адресов анонимному пользователю"""
        url_names = (
            '/',
            '/group/test-slug/',
            f'/profile/{USERNAME}/',
            f'/posts/{self.post.pk}/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.guest_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.OK, url_text_error)

    def test_page_exists_authorized_client(self):
        """Проверка доступности url-адресов авторизованному пользователю"""
        url_names = (
            '/',
            '/group/test-slug/',
            f'/profile/{USERNAME}/',
            f'/posts/{self.post.pk}/',
            f'/posts/{self.post.pk}/edit/',
            '/create/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.authorized_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.OK, url_text_error)

    def test_page_no_exists_anonymous(self):
        """Проверка не существующих url-адресов анонимному пользователю"""
        url_names = (
            '/test/',
            '/home/',
            '/group/test-slug2/',
            '/group/',
            '/profile/',
            '/profile/user/',
            '/posts/',
            '/posts/111/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.guest_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND, url_text_error)

    def test_page_no_exists_authorized_client(self):
        """Проверка не существующих url-адресов авторизованному пользователю"""
        url_names = (
            '/test/',
            '/home/',
            '/group/test-slug2/',
            '/group/',
            '/profile/',
            '/profile/user/',
            '/posts/',
            '/posts/111/',
            '/posts/edit/',
            '/posts/111/edit/',
            '/create/add/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.authorized_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND, url_text_error)

    def test_redirect_url_anonymous(self):
        """Проверка перенаправления страницы для анонимного пользователя."""
        url_names = {
            '/posts/1/edit/': '/auth/login/?next=/posts/1/edit/',
            '/posts/1115/edit/': '/auth/login/?next=/posts/1115/edit/',
            '/create/': '/auth/login/?next=/create/',
        }
        for url, redirect in url_names.items():
            with self.subTest(address=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            f'/profile/{USERNAME}/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }        
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
