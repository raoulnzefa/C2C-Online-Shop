# -*-coding:utf-8 -*-
import os
from app01 import models
from rest_framework import serializers


class AllGoodsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        fields = ['id', 'name', 'price', 'sub_title', 'image']

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.image))


class GoodsDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    seller = serializers.CharField(source='seller.username')
    detail = serializers.SerializerMethodField()
    small_image = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        fields = ['id', 'name', 'price', 'sub_title', 'image', 'seller', 'detail', 'small_image']

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.image))

    def get_detail(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.detail))

    def get_small_image(self, row):
        res = [os.path.join('http://127.0.0.1:8000/media/', str(row.image))]
        for i in row.small_image.all():
            res.append(os.path.join('http://127.0.0.1:8000/media/', str(i.image_url)))
        return res


class CartAddSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.num = validated_data.get('num')
        instance.save()
        return instance

    def create(self, validated_data):
        return models.Cart.objects.create(**validated_data)

    user_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    num = serializers.IntegerField()


class CartListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='goods.name')
    price = serializers.FloatField(source='goods.price')
    image = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='goods.id')

    class Meta:
        model = models.Cart
        fields = ['id', 'name', 'price', 'image', 'num']

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.goods.image))


class CartEditSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.num = validated_data.get('num')
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    user_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    num = serializers.IntegerField()


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id', 'name', 'phone', 'address']


class AddressAddEditSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.phone = validated_data.get('phone')
        instance.address = validated_data.get('address')
        instance.save()
        return instance

    def create(self, validated_data):
        return models.Address.objects.create(**validated_data)

    user_id = serializers.IntegerField()
    name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()


class OrderListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    seller = serializers.CharField(source='goods.seller.username')

    class Meta:
        model = models.Orders
        fields = '__all__'
        depth = 1

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.goods.image))


class SaleListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Orders
        fields = '__all__'
        depth = 1

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.goods.image))


class MyGoodsListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    small_image = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        fields = '__all__'
        depth = 1

    def get_image(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.image))

    def get_detail(self, row):
        return os.path.join('http://127.0.0.1:8000/media/', str(row.detail))

    def get_small_image(self, row):
        res = [os.path.join('http://127.0.0.1:8000/media/', str(row.image))]
        for i in row.small_image.all():
            res.append(os.path.join('http://127.0.0.1:8000/media/', str(i.image_url)))
        return res
