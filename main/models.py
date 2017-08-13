from django.conf import settings
from django.db import models


# Create your models here.

class Location(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    lnglat = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def lat(self):
        return self.lnglat.split(',')[1]

    def lng(self):
        return self.lnglat.split(',')[0]


class TextComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    message_response = models.TextField()
    location = models.ForeignKey(Location, related_name='location_set', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



class Money(models.Model):
    money = models.IntegerField()

class OrderBill(models.Model):
    order_bill = models.IntegerField()
