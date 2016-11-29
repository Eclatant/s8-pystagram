from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

class Profile(models.Model):
    _genders = (
        ('M', _('Male'),   ),
        ('F', _('Female'), ),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1,
                              null=True,
                              blank=True,
                              choices=_genders)

