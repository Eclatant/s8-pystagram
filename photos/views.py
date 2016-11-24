from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from django.views.generic import CreateView

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Post
from .models import Tag
from .forms import PostForm, CommentForm


def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    elif request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()     # modelform method는 저장된 model object의 instance 반환

            tag_text = form.cleaned_data.get('tagtext', '')    #cleaned_data['tags']로 사용가능하나, 빈문자열 있을시 에러 처리 불가능
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
    mode = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    # 다시 해당 페이지로 Redirect를 위해서는 다음과 같은 방법을 사용할 수 있다
    # 1. success_url =
    # 2. def get_success_url(self):
    # 3. 마지막으로 model install 에서 get_absolute_url method를 호출한다.


create_post = PostCreateView.as_view()


# Create your views here.
def list_posts(request):
    page = request.GET.get('page', 1)  # 1은 default로

    per_page = 2

    # 생성일시 역순으로 하고 일시가 같으면 pk 역순으로
#    posts = Post.objects.all().order_by('-created_at', '-pk')[start_page:end_page]
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
#        'posts': posts,             ## 임시로 comment를 풀었음. 조심할것
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


list_posts = PostListView.as_view()


def view_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method != 'POST':
        form = CommentForm()
    elif request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('photos:view', args=[post.pk]))

    ctx = {
        'post': post,
        'form': form,
    }
    return render(request, 'view.html', ctx)


# Tag 편집 미구현
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    content = post.content
#    tags = Tag.objects.get(pk=pk)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)

        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('photos:view', args=[post.pk]))

    ctx = {
        'post': post,
        'content': content,
#        'tags': tags,
        'form': form,
    }
    return render(request, 'edit_post.html', ctx)
