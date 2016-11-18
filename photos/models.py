from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category)
    content = models.TextField(null=False, blank=False)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('photos:view',
                            kwargs={'pk': self.pk})

    # class Meta:
    #     ordering = ('-created_at', '-id', )


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

