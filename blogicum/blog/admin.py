from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_published', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date',
                    'is_published', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'created_at')
    date_hierarchy = 'pub_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Отображаем начало текста, пост, автора и дату
    list_display = ('text', 'post', 'author', 'created_at')
    # Возможность фильтровать по дате и автору
    list_filter = ('created_at', 'author')
    # Поиск по тексту комментария
    search_fields = ('text',)
