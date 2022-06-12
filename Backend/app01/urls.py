# -*-coding:utf-8 -*-

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from app01 import views
from djangoProject import settings
from rest_framework import routers

urlpatterns = [

    path('home', views.HomeView.as_view()),
    path('allgoods', views.AllGoodView.as_view()),
    path('goodsDetail', views.GoodsDetailView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('user', views.UserView.as_view()),

    path('CartAdd', views.CartListAddView.as_view()),
    path('CartList', views.CartListAddView.as_view()),
    path('CartDelete', views.CartDeleteView.as_view()),
    path('CartEdit', views.CartEditView.as_view()),

    path('AddressAdd', views.AddressListAddView.as_view()),
    path('AddressList', views.AddressListAddView.as_view()),
    path('AddressEdit', views.AddressEditAddView.as_view()),
    path('AddressDelete', views.AddressDeleteAddView.as_view()),

    path('SubmitOrder', views.SubmitOrderView.as_view()),
    path('OrderList', views.OrderList.as_view()),

    path('Upload', views.UploadXXXView.as_view()),
    path('RelaseGoods', views.UploadGoodsView.as_view()),
    path('SaleList', views.SaleListView.as_view()),
    path('MyGoodsList', views.MyGoodsListView.as_view()),
    path('MyGoodsEdit', views.MyGoodsEditView.as_view()),


]
