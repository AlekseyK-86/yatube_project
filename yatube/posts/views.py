from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Post, Group


def index(request):
    template = 'posts/index.html'
    title = "Это главная страница проекта YaTube"
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'title': title,
        'text': 'Последние обновления на сайте!',
        'posts': posts,
    }
    return render(request, template, context)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = "Последние 10 постов группы"
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': title,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)

