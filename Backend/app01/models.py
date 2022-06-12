from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    head = models.FileField(max_length=64, upload_to='user_head', null=True, blank=True)


class UserToken(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Goods(models.Model):
    name = models.CharField(max_length=64, unique=False)
    price = models.FloatField(unique=False)
    sub_title = models.CharField(max_length=64, unique=False)
    image = models.FileField(max_length=128, upload_to='product_image', unique=False)
    seller = models.ForeignKey(to='Users', on_delete=models.CASCADE)
    detail = models.FileField(max_length=128, upload_to='product_detail', null=True, blank=True, unique=False)
    small_image = models.ManyToManyField(to='GoodDetailImages')


class GoodDetailImages(models.Model):
    image_url = models.FileField(max_length=128, upload_to='product_small_images')


class Cart(models.Model):
    user = models.ForeignKey(to='Users', on_delete=models.CASCADE)
    goods = models.ForeignKey(to='Goods', on_delete=models.CASCADE)
    num = models.IntegerField()


class Orders(models.Model):
    goods = models.ForeignKey(to='Goods', on_delete=models.CASCADE)
    num = models.IntegerField(null=True, blank=True)
    buyer = models.ForeignKey(to='Users', on_delete=models.CASCADE)
    address = models.ForeignKey(to='Address', on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey(to='Users', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=512)
