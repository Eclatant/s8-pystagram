from django import template

register = template.Library()

@register.filter(name='did_like')
def did_like(post, user):
    return post.like_set.filter(user=user).exists()

