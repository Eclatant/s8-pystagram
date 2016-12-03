from django import template
from django.template.base import VariableNode
from django.contrib.auth import get_user_model

register = template.Library()

@register.filter(name='did_like')
def did_like(post, user):
    return post.like_set.filter(user=user).exists()

@register.simple_tag
def helloworld(*args, **kwargs):
    return '<p>위치인자 {}</p><p>가변인자 {}</p>'.format(args, kwargs)


@register.tag(name='addnim')
def add_nim(parser, token):
    nodelist = parser.parse(('end_edd_nim', 'endaddnim', ))
    parser.delete_first_token()
    return NimNode(nodelist)


class NimNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.user_class = get_user_model()

    def render(self, context):
        outputs = []
        for node in self.nodelist:
            outputs.append(node.render(context))

            if isinstance(node, VariableNode):
                obj = node.filter_expression.resolve(context)
                if isinstance(obj, self.user_class):
                    outputs.append('님')

            # if not isinstance(obj, self.user_class):

            # if not isinstance(node, VariableNode):
            #     outputs.append(node.render(context))
            #     continue

            # obj = node.filter_expression.resolve(context)
            # if not isinstance(obj, self.user_class):
            #     outputs.append(node.render(context))
            #     continue

            # outputs.append('{}님'.format(node.render(context)))
        return ''.join(outputs)

