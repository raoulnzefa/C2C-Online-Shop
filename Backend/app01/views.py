import os
import json
from app01 import models
from app01.MyTools import serializer, pagination, auth
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        with open('app01/data/home.json', encoding='utf-8', mode='r') as f:
            home_data = json.load(f)
            return Response(home_data)


class AllGoodView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        params = request.query_params

        if not params.get('sort'):
            all_goods = models.Goods.objects.all()
        elif params.get('sort') == '1':
            all_goods = models.Goods.objects.all().order_by('price')
        elif params.get('sort') == '-1':
            all_goods = models.Goods.objects.all().order_by('-price')
        else:
            all_goods = models.Goods.objects.all()

        if params.get('price_gt'):
            all_goods = list(filter(lambda obj: obj.price > float(params.get('price_gt')), all_goods))
        if params.get('price_lt'):
            all_goods = list(filter(lambda obj: obj.price < float(params.get('price_lt')), all_goods))

        pg = pagination.MyPagination(params)
        pager_all_goods = pg.paginate_queryset(queryset=all_goods, request=request, view=self)
        ser = serializer.AllGoodsSerializer(instance=pager_all_goods, many=True)
        return pg.get_paginated_response(ser.data)


class GoodsDetailView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        good_obj = models.Goods.objects.filter(id=request.query_params['productId']).first()
        ser = serializer.GoodsDetailSerializer(instance=good_obj, many=False)
        return Response(ser.data)


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = request.data['username']
        pwd = request.data['password']
        obj = models.Users.objects.filter(username=user, password=pwd).first()
        if not obj:
            return Response({'code': 0, 'error': '用户名或密码错误'})
        token = auth.md5(user)
        models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        head = os.path.join('http://127.0.0.1:8000/media/', str(obj.head))
        return Response({
            'code': 1,
            'token': token,
            'user': user,
            'head': head
        })


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        repwd = request.data.get('rePassword')
        head = request.data.get('head')
        if pwd != repwd:
            return Response({'code': 300, 'error': '两次输入的密码不同'})
        if models.Users.objects.filter(username=user).first():
            return Response({'code': 400, 'error': '用户名已存在'})
        if not head:
            return Response({'code': 500, 'error': '请上传头像'})
        # 存入数据库
        new_user = {
            'username': user,
            'password': pwd,
            'head': 'user_head/' + str(head),
        }
        try:
            with open(f'media/{new_user["head"]}', 'wb') as f:
                for chunk in head.chunks():
                    f.write(chunk)

            models.Users.objects.create(**new_user)

            return Response({'code': 200, 'error': '两次输入的密码不同'})
        except:
            return Response({'code': 600, 'error': '注册失败'})


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        # print(request.user, request.auth)
        return Response('user')


class CartListAddView(APIView):
    def get(self, request, *args, **kwargs):
        cart_queryset = models.Cart.objects.filter(user=request.user).all()
        ser = serializer.CartListSerializer(instance=cart_queryset, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        goods_id = request.data.get('good_id')
        user = request.user
        num = request.data.get('product_num')
        data = {
            'goods_id': goods_id,
            'user_id': user.id,
            'num': num
        }
        old_goods = models.Cart.objects.filter(user=user, goods_id=goods_id).first()
        if old_goods:
            data['num'] += old_goods.num
            ser = serializer.CartAddSerializer(instance=old_goods, data=data)
        else:
            ser = serializer.CartAddSerializer(data=data)
        if ser.is_valid():
            ser.save()
        else:
            print(ser.errors)
        # 返回当前添加的这个商品信息
        cart_info = models.Cart.objects.filter(user=user, goods_id=goods_id).first()
        cart_ser = serializer.CartListSerializer(instance=cart_info, many=False)
        return Response(cart_ser.data)


class CartDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        goods_id = request.data.get('id')
        models.Cart.objects.filter(user=user, goods_id=goods_id).delete()
        return Response('删除成功')


class CartEditView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        goods_id = request.data.get('goods_id')
        num = request.data.get('product_num')
        data = {'user_id': user.id, 'goods_id': goods_id, 'num': num}
        instance = models.Cart.objects.filter(user=user, goods_id=goods_id).first()
        ser = serializer.CartEditSerializer(instance=instance, data=data)
        if ser.is_valid():
            ser.save()
        else:
            print(ser.errors)
        # 返回当前编辑的这个商品信息
        cart_info = models.Cart.objects.filter(user=user, goods_id=goods_id).first()
        cart_ser = serializer.CartListSerializer(instance=cart_info, many=False)
        return Response(cart_ser.data)


class AddressListAddView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        address_queryset = models.Address.objects.filter(user=user).all()
        ser = serializer.AddressListSerializer(instance=address_queryset, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('name')
        phone = request.data.get('phone')
        address = request.data.get('address')
        data = {
            'user_id': user.id,
            'name': name,
            'phone': phone,
            'address': address
        }
        ser = serializer.AddressAddEditSerializer(data=data)
        if ser.is_valid():
            ser.save()
        else:
            print(ser.errors)
        # 返回新建的那个地址
        address_obj = models.Address.objects.filter(**data).first()
        ser = serializer.AddressListSerializer(instance=address_obj, many=False)
        return Response(ser.data)


class AddressEditAddView(APIView):
    def post(self, request, *args, **kwargs):
        addr_id = request.data.get('id')
        user = request.user
        name = request.data.get('name')
        phone = request.data.get('phone')
        address = request.data.get('address')
        data = {
            'user_id': user.id,
            'name': name,
            'phone': phone,
            'address': address
        }
        old_obj = models.Address.objects.filter(id=addr_id).first()
        edit_ser = serializer.AddressAddEditSerializer(instance=old_obj, data=data)
        if edit_ser.is_valid():
            edit_ser.save()
        else:
            print(edit_ser.errors)
        new_obj = models.Address.objects.filter(id=addr_id).first()
        ser = serializer.AddressListSerializer(instance=new_obj, many=False)
        return Response(ser.data)


class AddressDeleteAddView(APIView):
    def post(self, request, *args, **kwargs):
        addr_id = request.data.get('id')
        models.Address.objects.filter(id=addr_id).delete()
        return Response('删除成功')


class SubmitOrderView(APIView):
    def post(self, request, *args, **kwargs):
        buyer = request.user
        addr_id = request.data.get('addrId')
        cartList = request.data.get('cartList')
        try:
            for goods in cartList:
                order_data = {
                    'buyer': buyer,
                    'address_id': addr_id,
                    'goods_id': goods.get('id'),
                    'num': goods.get('num')
                }
                models.Orders.objects.create(**order_data)
            return Response(200)
        except:
            return Response(400)


class OrderList(APIView):
    def get(self, request, *args, **kwargs):
        order_queryset = models.Orders.objects.filter(buyer=request.user).all()
        params = request.query_params

        pg = pagination.MyPagination(params)
        pager_queryset = pg.paginate_queryset(queryset=order_queryset, request=request, view=self)
        ser = serializer.OrderListSerializer(instance=pager_queryset, many=True)

        return pg.get_paginated_response(ser.data)


class UploadXXXView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        return Response(123)


class UploadGoodsView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get('name')
        price = request.data.get('price')
        sub_title = request.data.get('price')
        image = request.data.get('image')
        detail = request.data.get('detail')
        smallImage = request.data.getlist('smallImage')  # list
        if name and price and sub_title and image and detail and smallImage:
            pass
        else:
            return Response(400)
        goods_data = {
            'name': name,
            'price': price,
            'sub_title': sub_title,
            'image': 'product_image/' + auth.md5(str(image)),
            'seller': user,
            'detail': 'product_detail/' + auth.md5(str(detail))
        }
        try:
            with open(f'media/{goods_data["image"]}', 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            with open(f'media/{goods_data["detail"]}', 'wb') as f:
                for chunk in detail.chunks():
                    f.write(chunk)

            new_goods_obj = models.Goods.objects.create(**goods_data)

            for small_img in smallImage:
                url = 'product_small_images/' + auth.md5(str(small_img)),

                with open(f'media/{url[0]}', 'wb') as f:
                    for chunk in small_img.chunks():
                        f.write(chunk)

                small_image_obj = models.GoodDetailImages.objects.create(image_url=url[0])
                new_goods_obj.small_image.add(small_image_obj)

            return Response(200)
        except:
            return Response(400)


class SaleListView(APIView):
    def get(self, request, *args, **kwargs):
        sale_queryset = models.Orders.objects.filter(goods__seller=request.user).all()
        params = request.query_params

        pg = pagination.MyPagination(params)
        pager_queryset = pg.paginate_queryset(queryset=sale_queryset, request=request, view=self)
        ser = serializer.SaleListSerializer(instance=pager_queryset, many=True)

        return pg.get_paginated_response(ser.data)


class MyGoodsListView(APIView):
    def get(self, request, *args, **kwargs):
        my_goods_queryset = models.Goods.objects.filter(seller=request.user).all()
        params = request.query_params

        pg = pagination.MyPagination(params)
        pager_queryset = pg.paginate_queryset(queryset=my_goods_queryset, request=request, view=self)
        ser = serializer.MyGoodsListSerializer(instance=pager_queryset, many=True)

        return pg.get_paginated_response(ser.data)


class MyGoodsEditView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        goods_id = request.data.get('id')
        name = request.data.get('name')
        price = request.data.get('price')
        sub_title = request.data.get('price')
        image = request.data.get('image')
        detail = request.data.get('detail')
        smallImage = request.data.getlist('smallImage')
        edit_data = {
            'id': goods_id,
            'name': name,
            'price': price,
            'sub_title': sub_title,
        }
        try:
            if image:
                edit_data['image'] = 'product_image/' + auth.md5(str(image))
                with open(f'media/{edit_data["image"]}', 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            if detail:
                edit_data['detail'] = 'product_detail/' + auth.md5(str(detail))
                with open(f'media/{edit_data["detail"]}', 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

            obj = models.Goods.objects.filter(id=goods_id)
            obj.update(**edit_data)

            if smallImage:
                old_small_img = models.GoodDetailImages.objects.filter(goods=obj.first())
                old_small_img.delete()

                for small_img in smallImage:
                    url = 'product_small_images/' + auth.md5(str(small_img)),

                    with open(f'media/{url[0]}', 'wb') as f:
                        for chunk in small_img.chunks():
                            f.write(chunk)
                    small_image_obj = models.GoodDetailImages.objects.create(image_url=url[0])
                    obj.first().small_image.add(small_image_obj)
            return Response(200)
        except:
            return Response(400)


