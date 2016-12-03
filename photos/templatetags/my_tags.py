from django import template

register = template.Library()

@register.filter(name='did_like')
def did_like(post, user):
    return post.like_set.filter(user=user).exists()

@register.simple_tag
def helloworld(*args, **kwargs):
    return '<p>위치인자 {}</p><p>가변인자 {}</p>'.format(args, kwargs)

