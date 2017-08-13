from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class innerUserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'innerUserInfo_set')
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
