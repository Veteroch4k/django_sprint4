from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator  # <--- ВАЖНЫЙ ИМПОРТ
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .forms import CommentForm


def index(request):
    """Главная страница."""
    post_list = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')

    # Настраиваем пагинацию (10 постов на страницу)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # В шаблон передаем page_obj
    return render(request, 'blog/index.html', {'page_obj': page_obj})


# 1. ОБНОВЛЕННЫЙ post_detail (теперь с формой и комментами)
def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        pk=pk,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

    # Форма для добавления комментария
    form = CommentForm()

    # Список комментариев к посту
    # (Если в модели Comment поле post имеет related_name='comments', то так:)
    comments = post.comments.select_related('author')
    # (Если related_name нет, пишите: post.comment_set.select_related('author'))

    context = {
        'post': post,
        'form': form,  # Передаем форму в шаблон
        'comments': comments  # Передаем список комментариев
    }
    return render(request, 'blog/detail.html', context)


# 2. ДОБАВЛЕНИЕ КОММЕНТАРИЯ
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


# 3. УДАЛЕНИЕ ПОСТА
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # Django запросит подтверждение. Обычно используют тот же шаблон create.html
    # или отдельный delete.html. Давайте пока используем create.html,
    # но Django ожидает post_confirm_delete.html по умолчанию.
    # Проще создать файл templates/blog/post_confirm_delete.html (см. шаг 4 ниже)

    # Но если хотите использовать form_class или просто удалить без вопросов (не рекомендуется),
    # то нужна логика. Стандартный путь — шаблон подтверждения.
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=instance.pk)
        return super().dispatch(request, *args, **kwargs)

    # После удаления — в профиль
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})
def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'author', 'location'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def profile(request, username):
    """Профиль пользователя."""
    profile_user = get_object_or_404(User, username=username)

    post_list = Post.objects.filter(author=profile_user).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile_user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=instance.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Редактировать может только автор
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=instance.post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Возвращаемся на страницу поста (post.pk берем из самого комментария)
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Удалять может только автор
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=instance.post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})