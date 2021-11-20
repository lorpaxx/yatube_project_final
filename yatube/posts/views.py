from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import cache_page

from .models import Follow, Group, Post, User, Comment
from .forms import PostForm, CommentForm

from yatube.settings import COUNT_OF_PAGE_POST, TIME_CACHED


@cache_page(TIME_CACHED, key_prefix='index_page')
def index(request):
    '''
    Функция вызова заглавной страницы.
    '''
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, COUNT_OF_PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    '''
    Функция вызова страницы сообщества.
    '''
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, COUNT_OF_PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    '''
    Функция вызова страницы пользователя.
    '''
    template = 'posts/profile.html'
    profile_user = get_object_or_404(User, username=username)
    name_user = profile_user.get_full_name()
    title_profile = f'Профайл пользователя {name_user}'
    post_list = profile_user.posts.all()
    paginator = Paginator(post_list, COUNT_OF_PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.follower.filter(author=profile_user).exists()

    context = {
        'title': title_profile,
        'profile_user': profile_user,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    '''
    Функция вызова страницы конкретного поста.
    '''
    template = 'posts/post_details.html'
    current_post: Post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    title_post_detail = f'Пост {current_post}'
    comments = Comment.objects.filter(post=current_post)
    context = {
        'title': title_post_detail,
        'post': current_post,
        'form': form,
        'comments': comments
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    '''
    Функция добавления комментария.
    '''
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def post_create(request):
    '''
    Функция вызова страницы создания нового поста.
    '''
    template = 'posts/create_post.html'

    if request.method != 'POST':
        form = PostForm(files=request.FILES or None)
        return render(
            request, template,
            {'title': 'Новый пост', 'form': form, 'is_edit': False}
        )

    form = PostForm(request.POST, files=request.FILES or None)

    if not form.is_valid():
        return render(
            request, template,
            {'title': 'Новый пост', 'form': form, 'is_edit': False}
        )

    user = request.user
    new_post = form.save(commit=False)
    new_post.author = user
    new_post.save()
    return redirect('posts:profile', username=user.username)


@login_required
def post_edit(request, post_id):
    '''
    Функция редактирования существующего поста.
    '''
    template = 'posts/create_post.html'
    title = 'Редактируемый пост'
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    if request.method != 'POST':
        form = PostForm(
            files=request.FILES or None,
            instance=post
        )
        return render(
            request, template,
            {'title': title, 'form': form, 'is_edit': True}
        )

    form = PostForm(
        request.POST,
        files=request.FILES or None,
        instance=post
    )
    if not form.is_valid():
        return render(
            request, template,
            {'title': title, 'form': form, 'is_edit': True}
        )

    form.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    '''
    Отображет те посты, на которые подписан user.
    '''
    template = 'posts/follow.html'
    user: User = request.user
    follows = user.follower.all()
    authors = list(follow.author for follow in follows)
    post_list = Post.objects.filter(author__in=authors)
    paginator = Paginator(post_list, COUNT_OF_PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    '''
    user подписывается на автора username.
    '''
    user = request.user
    author = get_object_or_404(User, username=username)
    check_follow = Follow.objects.filter(user=user, author=author).exists()
    if (not check_follow) and (user != author):
        new_follow = Follow.objects.create(user=user, author=author)
        new_follow.save()
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    '''
    user отписывается от автора username.
    '''
    user = request.user
    author = get_object_or_404(User, username=username)
    check_follow = Follow.objects.filter(user=user, author=author).exists()
    if check_follow:
        follow = Follow.objects.get(user=user, author=author)
        follow.delete()
    return redirect('posts:profile', username=username)
