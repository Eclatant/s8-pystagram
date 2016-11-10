from django.shortcuts import render

#from photos.models import Post
from .models import Post


def list_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    ctx = {
        'posts': posts,
    }
    return render(request, 'list.html', ctx)


