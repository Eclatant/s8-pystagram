import os
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import serializers as drf_serializers
from rest_framework import viewsets

#from photos.models import Post
from .models import Post
from .models import Tag
from .models import Comment
from .models import Like
from .forms import PostForm
from .forms import CommentForm
from pystagram.sample_exceptions import HelloWorldError


logger = logging.getLogger('django')


import base64


def get_base64_image(data):
    if data is None or ';base64,' not in data:
        return None

    _format, _content = data.split(';base64,')
    return base64.b64decode(_content)


@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    elif request.method == 'POST':
        filtered = request.POST.get('filtered_image')
        if filtered:
            filtered_image = get_base64_image(filtered)
            filename = request.FILES['image'].name.split(os.sep)[-1]
            _filedata = {
                'image': SimpleUploadedFile(
                    filename, filtered_image
                )
            }
        else:
            _filedata = request.FILES

        form = PostForm(request.POST, _filedata)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            tag_text = form.cleaned_data.get('tagtext', '')
            tags = tag_text.split(',')
            for _tag in tags:
                _tag = _tag.strip()
                tag, _ = Tag.objects.get_or_create(name=_tag, defaults={'name': _tag})
                post.tags.add(tag)

            return redirect('photos:view', pk=post.pk)

    ctx = {
        'form': form,
    }
    return render(request, 'edit_post.html', ctx)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

#create_post = PostCreateView.as_view()


def list_posts(request):
    #logger.error('lorem ipsum', exc_info=True, extra={'request': request}) 
    #logger.warning('경고 경고')
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

    if request.is_ajax():
        data = serializers.serialize('json', contents)
        return HttpResponse(data)

    ctx = {
        'posts': contents,
    }
    return render(request, 'list.html', ctx)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'list.html'
    paginate_by = 2
    # queryset = Post.objects.order_by('-created_at')

    def get_queryset(self):
        return Post.objects.order_by('-created_at')

#list_posts = PostListView.as_view()


@login_required
def view_post(request, pk):
    key = 'post_object_{}'.format(pk)
    post = cache.get(key)
    if not post:
        post = Post.objects.get(pk=pk)
        cache.set(key, post, 300)
        print('get data from db')
    else:
        print('get cahced data')

    if request.method == 'GET':
        form = CommentForm()
    elif request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect(post)  # Post 모델의 `get_absolute_url()` 메서드 호출
            # return redirect('photos:view', pk=post.pk)

    ctx = {
        'post': post,
        'comment_form': form,
    }
    return render(request, 'view.html', ctx)


def delete_comment(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest()

    comment = get_object_or_404(Comment, pk=pk)

    comment.delete()

    return redirect(comment.post)  # Post 모델의 `get_absolute_url()` 메서드 호출

@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'GET':
        form = PostForm(instance=post)
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(post)  # Post 모델의 `get_absolute_url()` 메서드 호출
            # return redirect('photos:view', pk=post.pk)

    ctx = {
        'post': post,
        'form': form,
    }
    return render(request, 'edit_post.html', ctx)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method != 'POST':
        raise Exception('bad request')

    qs = post.like_set.filter(user=request.user)
    if qs.exists():
        like = qs.get()
        like.delete()
    else:
        like = Like()
        like.post = post
        like.user = request.user
        like.save()

    return redirect(post)


class PostSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['category', 'content', ]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




