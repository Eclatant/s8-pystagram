# Script fill db contents ver 0.1
# run ./manage.py shell < photos.prebuild.py
# after db migration

from photos.models import *

tags = ['Django', 'python', 'Facebook', 'science', 'flask', ]
categories = ['Politics', 'Math', 'Social', 'Muaic', 'International', ]

for t in tags:
    Tag(name=t).save()

root = Category(name='Root')
root.save()
for c in categories:
    Category(name=c, parent=root).save()

cats = Category.objects.all()
for idx in range(10):
    for c in cats:
        Post(content='{} {} th 글입니다.'.format(c.name, idx+1), category=c).save()

for p in Post.objects.all():
    for idx in range(3):
        Comment(content='댓글 {} th 글입니다.'.format(idx+1), post=p).save()

# for idx, p in enumerate(Category.objects.all()):
#     print(idx, p.name)
