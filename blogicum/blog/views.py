from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.models import User



def index(request):
    """Главная страница: 5 последних опубликованных постов."""
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, pk):
    """Страница отдельного поста."""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        pk=pk,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, slug):
    """Страница категории: посты из указанной категории."""
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    posts = Post.objects.select_related(
        'author', 'location'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )


def profile(request, username):
    # Ищем пользователя по никнейму, если нет — 404
    profile_user = get_object_or_404(User, username=username)

    # Выбираем посты этого пользователя

    user_posts = Post.objects.filter(author=profile_user)

    context = {
        'profile': profile_user,
        'posts': user_posts,
    }
    return render(request, 'blog/profile.html', context)


# Редактирование профиля
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user


    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    # Указываем поля, которые пользователь заполняет сам
    # (image добавляем, так как по заданию нужны картинки)
    fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']

    # Автоматически сохраняем автора
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # После успеха перенаправляем на профиль
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})