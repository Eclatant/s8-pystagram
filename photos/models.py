from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', null=True)

    def __str__(self):
        return self.name

from django.contrib.contenttypes.fields import GenericRelation

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category)
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='%Y/%m/%d/', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like2')

    def __str__(self):
        return '{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('photos:view',
                            kwargs={'pk': self.pk})

    # # In this case, QuerySet delete doesn't call this function
    # def delete(self, *args, **kwargs):
    #     super(Post, self).delete(*args, **kwargs)
    #     self.image.delete(commit=False)

    # class Meta:
    #     ordering = ('-created_at', '-id', )


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like2')

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Like2(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

@receiver(post_delete, sender=Post)
def delete_attahement_image(sender, instance, **kwargs):
    if not instance.image:
        return
    instance.image.delete(save=False)

# without decorator
# post_delete.content_object(delete_attahement_image, sender=Post)
