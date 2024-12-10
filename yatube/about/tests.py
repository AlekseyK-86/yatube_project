from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from yatube.posts.constants import USERNAME


User = get_user_model()


class PostURLTests(TestCase):
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

    def test_page_no_exists_anonymous(self):
        """Проверка доступности url-адресов анонимному пользователю"""
        url_names = (
            '/about/',
            '/about/tech2/',
            '/about/author2/',
            '/about/tech/2',
            '/about/author/2',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.guest_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND, url_text_error)
    
    def test_page_no_exists_authorized_client(self):
        """Проверка доступности url-адресов авторизованному пользователю"""
        url_names = (
            '/about/',
            '/about/tech2/',
            '/about/author2/',
            '/about/tech/2',
            '/about/author/2',
        )
        for url in url_names:
            with self.subTest(address=url):
                response = self.authorized_client.get(url)
                url_text_error = f'URL-адрес {url} отработал не верно, нужно проверить.'
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND, url_text_error)
    
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        page_names_templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for reverse_name, template in page_names_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
