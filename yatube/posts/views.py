from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from posts.forms import PostForm


def index(request):
    template = 'posts/index.html'
    title = "Это главная страница проекта YaTube"
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj
    }

    return render(request, template, context)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = "Последние 10 постов группы"
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, template, context)

def profile(request, username):
    title = f"Профайл пользователя: {username}"
    user_name = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_name.id).all().order_by('-pub_date')
    post_count = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user_name == request.user:
        post_author = request.user
    else:
        post_author = ""
        
    context = {
        'title': title,
        'username': user_name,
        'post_count': post_count,
        'page_obj': page_obj,
        'post_author': post_author
    }

    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=post.author.id).count()

    if post.author == request.user:
        post_author = request.user
    else:
        post_author = ""
    
    context = {
        'post': post,
        'post_count': post_count,
        'post_author': post_author
    }

    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    title = "Создание нового поста"

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    else:
        form = PostForm()

    context = {
        'title': title,
        'form': form
    }

    return render(request, 'posts/create_post.html', context)

@login_required
def post_edit(request, post_id):
    title = "Редактировать запись"
    is_edit = get_object_or_404(Post, id=post_id)

    if is_edit.author != request.user:
        return redirect('posts:post_detail', post_id=is_edit.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=is_edit)
        if form.is_valid():
            is_edit = form.save()
            return redirect('posts:post_detail', post_id=is_edit.id)
    else:
        form = PostForm(instance=is_edit)
    
    context = {
        'title': title,
        'form': form,
        'is_edit': is_edit
    }

    return render(request, 'posts/create_post.html', context)
