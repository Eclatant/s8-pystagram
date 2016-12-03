from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Post

@receiver(post_delete, sender=Post)
def delete_attahement_image(sender, instance, **kwargs):
    if not instance.image:
        return
    instance.image.delete(save=False)

# without decorator
# post_delete.content_object(delete_attahement_image, sender=Post)
