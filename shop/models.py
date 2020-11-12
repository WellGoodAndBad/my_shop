from django.db import models
from django.conf import settings


class ItemShop(models.Model):
    article = models.IntegerField()
    name_item = models.TextField(max_length=1000, blank=True)
    purchase_price = models.FloatField(max_length=250, blank=True)
    shop_price = models.FloatField(max_length=250, blank=True)

    def __str__(self):
        return self.name_item


class UserCart(models.Model):
    items = models.ManyToManyField(ItemShop, related_name='items', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email

