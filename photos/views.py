from django.shortcuts import render


def list_posts(request):
    ctx = {}
    return render(request, 'list.html', ctx)


