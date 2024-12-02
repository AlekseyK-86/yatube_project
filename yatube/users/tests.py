from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

User = get_user_model()


class PostURLTests(TestCase):

    global USERNAME
    USERNAME = 'NoName'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)

    def setUp(self):
        self.guest_client = Client()
        self.user = PostURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_exists_anonymous(self):
        """Проверка доступности url-адресов анонимному пользователю"""
        url_names = (
            '/about/author/',
            '/about/tech/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.guest_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.OK, url_text_error)
    
    def test_page_exists_authorized_client(self):
        """Проверка доступности url-адресов авторизованному пользователю"""
        url_names = (
            '/about/author/',
            '/about/tech/',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.authorized_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.OK, url_text_error)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        page_names_templates = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:login'): 'users/login.html',
        }
        for reverse_name, template in page_names_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
