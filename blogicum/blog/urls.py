from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path(
        'category/<slug:slug>/',
        views.category_posts,
        name='category_posts'
    ),

    path('edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),

    # 2. Профиль пользователя (например: /profile/admin/)
    path('profile/<str:username>/', views.profile, name='profile'),

    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),

    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),

    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),

    # Добавление комментария
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('posts/<int:post_id>/edit_comment/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]
