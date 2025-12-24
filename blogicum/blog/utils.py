from django.utils import timezone

from .models import Post


def get_published_posts():
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
