from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

#from photos.models import Post
from .models import Post
from .forms import PostForm


def create_post(request):
    form = PostForm()
    ctx = {
        'form': form,
    }
    return render(request, 'edit_post.html', ctx)


def list_posts(request):
    page = request.GET.get('page', 1)
    per_page = 2

    posts = Post.objects \
                .all() \
                .order_by('-created_at', '-pk')

    pg = Paginator(posts, per_page)
    try:
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts': contents,
    }
    return render(request, 'list.html', ctx)


def view_post(request, pk):
    post = Post.objects.get(pk=pk)
    ctx = {
        'post': post,
    }
    return render(request, 'view.html', ctx)









