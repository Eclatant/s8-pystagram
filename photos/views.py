from django.shortcuts import render

#from photos.models import Post
from .models import Post


def list_posts(request):
    try:
        page = int(request.GET.get('page', 1))
    except Exception:
        page = 1
    finally:
        if page < 0:
            page = 1

    per_page = 2

    start_page = (page-1) * per_page
    end_page = page * per_page

    posts = Post.objects \
                .all() \
                .order_by('-created_at', '-pk')[start_page:end_page]

    ctx = {
        'posts': posts,
    }
    return render(request, 'list.html', ctx)


