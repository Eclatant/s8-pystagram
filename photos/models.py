from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', null=True)  # class가 아직 생성이 되지 않았던 관계로 이것도 문자열로 처리
    # null이면 parent 바로 자신이다

    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    category = models.ForeignKey(Category, default=1)
    # DB에 null은 허용하지 않고 form에서도 blank를 받지 않겠다
    content = models.TextField(null=False, blank=False)  # 첫번째 인자에 Label을 넣을수 있음
    # Tag가 먼지 몰라서 에러가 날 수 있다. 따라서 class Tag를 위로 올려야 한다
    tags = models.ManyToManyField('Tag', blank=True)
    # 이를 해결하기 위해 문자열  ' ' 로 묶어 처리
    # appName.ModelName 으로 하면 다른 app의 모델을 사용할 경우
    created_at = models.DateTimeField(auto_now_add=True)  # DB에 입력시 DB가 알아서l
    updated_at = models.DateTimeField(auto_now=True)  # save() 가 호출시에 자동으로

    def __str__(self):
        return '{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('photos:view',
                            kwargs={'pk': self.pk})

#    class Meta:
#        ordering = ('-created_at', '-id', )


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

