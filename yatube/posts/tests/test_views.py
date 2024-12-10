from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from yatube.posts.models import Post, Group
from yatube.posts.constants import USERNAME

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
        self.user = PostURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
    
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {            
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (reverse('posts:group_list', kwargs= {'slug': 'test-slug'})),
            'posts/profile.html': (reverse('posts:profile', kwargs= {'username': USERNAME})),
            'posts/post_detail.html': (reverse('posts:post_detail', kwargs= {'post_id': self.post.pk})),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
    
    def test_post_edit_page_uses_correct_template(self):
        """URL-адрес использует шаблон posts/create_post.html."""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs= {'post_id': self.post.pk}))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_create_page_uses_correct_template(self):
        """URL-адрес использует шаблон posts/create_post.html."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTemplateUsed(response, 'posts/create_post.html')

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

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        page_names_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': self.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in page_names_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон главной страницы сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post_text = response.context.get('page_obj')[0].text
        post_author = response.context.get('page_obj')[0].author.username
        group_post = response.context.get('page_obj')[0].group.title
        self.assertEqual(post_text, 'Тестовый пост post')
        self.assertEqual(post_author, USERNAME)
        self.assertEqual(group_post, 'Тестовая группа')

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        group_title = response.context.get('group').title
        group_slug = response.context.get('group').slug
        group_description = response.context.get('group').description
        self.assertEqual(group_title, 'Тестовая группа')
        self.assertEqual(group_slug, self.group.slug)
        self.assertEqual(group_description, 'Тестовое описание')

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': USERNAME}))
        post_text = response.context.get('page_obj')[0].text
        post_group = response.context.get('page_obj')[0].group.title 
        post_author = response.context.get('page_obj')[0].author.username 
        self.assertEqual(post_text, 'Тестовый пост post')
        self.assertEqual(post_group, self.group.title)
        self.assertEqual(post_author, USERNAME)
    
    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        post_text = response.context.get('post').text
        post_group = response.context.get('post').group.title 
        post_author = response.context.get('post').author.username 
        self.assertEqual(post_text, 'Тестовый пост post')
        self.assertEqual(post_group, self.group.title)
        self.assertEqual(post_author, USERNAME)
    
    def test_post_edit_show_correct_context(self):
        """Шаблон редактирования post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': self.post.pk}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field, expected in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_correct_context(self):
        """Шаблон создания поста create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field, expected in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_home_group_list_profile_pages(self):
        """Созданный пост отобразился на главной странице, 
        на странице группы и в профиле пользователя."""
        urls = (
            reverse('posts:index'),            
            reverse('posts:profile', kwargs={'username': USERNAME}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )        
        for url in urls:
            response = self.authorized_client.get(url)
            len_obj = len(response.context['page_obj'].object_list)
            self.assertEqual(len_obj, 1)

    def test_post_not_another_group(self):
        """Созданный пост не попал в группу, для которой не был предназначен"""
        another_group = Group.objects.create(
            title='тестовая группа вторая',
            slug='test-another-slug',
            description='Тестовое описание второй группы',
        )
        reverse_url = reverse('posts:group_list', kwargs={'slug': another_group.slug})
        response = self.authorized_client.get(reverse_url)
        len_obj = len(response.context['page_obj'])
        self.assertEqual(len_obj, 0)

class PaginatorViewsTest(TestCase):

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
        cls.post = [Post.objects.create(
            author = cls.user,
            text = f'Тестовый пост post {i}',
            group = cls.group
        )
        for i in range(13)]

    def setUp(self):
        self.user = PaginatorViewsTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Количество постов на страницах index, group_list, profile равно 10."""
        urls = (
            reverse('posts:index'),            
            reverse('posts:profile', kwargs={'username': USERNAME}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        for url in urls:
            response = self.authorized_client.get(url)
            len_obj = len(response.context['page_obj'].object_list)
            self.assertEqual(len_obj, 10)

    def test_second_page_contains_three_records(self):
        """Количество постов на вторых страницах index, group_list, profile равно 3."""
        urls = (
            reverse('posts:index') + '?page=2',            
            reverse('posts:profile', kwargs={'username': USERNAME}) + '?page=2',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2',
        )
        for url in urls:
            response = self.authorized_client.get(url)
            len_obj = len(response.context['page_obj'].object_list)
            self.assertEqual(len_obj, 3)
