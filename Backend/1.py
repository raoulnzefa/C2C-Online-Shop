# -*-coding:utf-8 -*-
# from django.shortcuts import render, HttpResponse
# from rest_framework import serializers
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.renderers import JSONRenderer
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
# from rest_framework.generics import GenericAPIView
# from rest_framework.viewsets import GenericViewSet, ModelViewSet
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
# from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer, HTMLFormRenderer
# =======================================DEF Study=====================================================================


# class BookInfoViewSet(ModelViewSet):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer


# class BookSerializer(serializers.Serializer):
#     # id = serializers.IntegerField()
#     title = serializers.CharField()
#     author = serializers.CharField()


# class BookView(APIView):
#     def get(self, request, *args, **kwargs):
#         book = models.BookInfo.objects.all()
#         ser = BookSerializer(instance=book, many=True)
#         res = json.dumps(ser.data, ensure_ascii=False)
#         return HttpResponse(res)


# ===============================User表=================================================
# class UserSerializer(serializers.Serializer):
#     usr_type = serializers.CharField(source='get_user_type_display')
#     user_name = serializers.CharField()
#     password = serializers.CharField()
#     book = serializers.CharField(source='book.title')
#     role = serializers.SerializerMethodField()
#
#     def get_role(self, row):
#         role_obj_list = row.role.all()
#         res = []
#         for item in role_obj_list:
#             # res.append({'id':item.id, 'role':item.get_role_display()})
#             res.append(item.get_role_display())
#         return res


# class UserModelSerializer(serializers.ModelSerializer):
#     usr_type = serializers.CharField(source='get_user_type_display')
#     role = serializers.SerializerMethodField()
#     book = serializers.CharField(source='book.title')
#
#     class Meta:
#         model = models.UserInfo
#         fields = ['id', 'user_name', 'usr_type', 'role', 'book']
#
#     def get_role(self, row):
#         role_obj_list = row.role.all()
#         res = []
#         for item in role_obj_list:
#             res.append(item.get_role_display())
#         return res


# class UserInfoView(APIView):
#     class UserDepthModelSerializer(serializers.ModelSerializer):
#         # book = serializers.SerializerMethodField()
#         book = serializers.HyperlinkedIdentityField(view_name='bk')
#
#         class Meta:
#             model = models.UserInfo
#             fields = ['user_name', 'book']
#             depth = 1
#
#         # def get_book(self, row):
#         #     return [f'http:127.0.0.1:8000/book/{row.book.id}']
#
#     def get(self, request, *args, **kwargs):
#         users = models.UserInfo.objects.all()
#         ser = self.UserDepthModelSerializer(instance=users, many=True, context={'request': request})
#         # res = json.dumps(ser.data, ensure_ascii=False)
#         res = JSONRenderer().render(ser.data)
#         return HttpResponse(res)


# class BookInfoView(APIView):
#     class BookInfoModelSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = models.BookInfo
#             fields = ['id', 'title', 'author']
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         obj = models.BookInfo.objects.filter(pk=pk).first()
#         ser = self.BookInfoModelSerializer(instance=obj, many=False)
#         res = JSONRenderer().render(ser.data)
#         return HttpResponse(res)


# ===============================表单验证=================================================
# class UserBookSerializer(serializers.Serializer):
#     title = serializers.CharField(error_messages={'required': 'title is empty'})
#
#     def validated_title(self):
#         pass
#
#
# class UserBookView(APIView):
#     def post(self, request, *args, **kwargs):
#         ser = UserBookSerializer(data=request.data)
#         if ser.is_valid():
#             print(ser.validated_data)
#         else:
#             print(ser.errors)


# ===============================分页=================================================


# 普通分页，offset开始，limit数量，加密分页

# class MyPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 50
#
#     page_query_param = 'page'
#
#
# class PagerView(APIView):
#     class PagerModelSerializer(serializers.ModelSerializer):
#         role = serializers.CharField(source='get_role_display')
#
#         class Meta:
#             model = models.Role
#             fields = ['id', 'role']
#
#     def get(self, request, *args, **kwargs):
#         roles = models.Role.objects.all()
#         pg = MyPagination()
#         pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
#         ser = self.PagerModelSerializer(instance=pager_roles, many=True)
#         return pg.get_paginated_response(ser.data)
#         # return Response(ser.data)


# ===============================View=================================================


# class PagerModelSerializer(serializers.ModelSerializer):
#     role = serializers.CharField(source='get_role_display')
#
#     class Meta:
#         model = models.Role
#         fields = ['id', 'role']
#
#
# class ViewView(ModelViewSet):
#     queryset = models.Role.objects.all()
#     serializer_class = PagerModelSerializer
#     pagination_class = PageNumberPagination

# ===============================view总结=================================================
# APIView 完全自定义
# GenericViewSet 在路由的地方可以把get分成不同的函数
# ModelViewSet，增删改查

# ===============================路由=================================================
# ===============================渲染器=================================================

# class TestView(APIView):
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     def get(self, request, *args, **kwargs):
#         pass

# ===============================认证=================================================
# from rest_framework.request import Request
# from rest_framework import exceptions
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.authentication import BaseAuthentication


# class OrderView(APIView):
#
#     def get(self, request, *args, **kwargs):
#
#         res = {'code': 200, 'msg': 'ppp', 'data': None}
#         try:
#             res['data'] = '订单'
#         except Exception as e:
#             pass
#         return Response(res)


# a = [1, 2, 3, 4, 5]
# b = filter(lambda x: x > 2, a)
# print(list(b))


# ====================================================================================================================


# Create your models here.

# class BookInfo(models.Model):
#     title = models.CharField(max_length=32)
#     author = models.CharField(max_length=16)
#
# class UserInfo(models.Model):
#     user_type_choice = (
#         (1, '普通用户'),
#         (2, 'VIP'),
#         (3, 'SVIP'),
#     )
#     user_type = models.IntegerField(choices=user_type_choice)
#     user_name = models.CharField(max_length=32, unique=True)
#     password = models.CharField(max_length=64)
#     book = models.ForeignKey(to='BookInfo', to_field='id',
#                              on_delete=models.SET_NULL, null=True, blank=True, related_name='book')
#     # role = models.ManyToManyField(to='Role')
#
#
# class UserToken(models.Model):
#     user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
#     token = models.CharField(max_length=64)

# class Role(models.Model):
#     role_choice = (
#         (1, 'student'),
#         (2, 'doctor'),
#         (3, 'teacher'),
#     )
#     role = models.IntegerField(choices=role_choice)


# ====================================================================================================================
def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


for i in range(4):
    a = md5('ppp')
    print(a)
    print(type(a))
