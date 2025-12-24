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

    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
]
