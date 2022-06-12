"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from djangoProject import settings
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('api/', include('app01.urls')),
    # path('home', views.HomeView.as_view()),
    # path('allgoods', views.AllGoodView.as_view()),
]

# router = routers.DefaultRouter()
# router.register(r'xxxx.json', views.ViewView)
# router.register(r'rt', views.ViewView)
# urlpatterns += router.get_urls()
#
# url_stydy = [
#     path('book', views.BookView.as_view()),
#     path('user', views.UserInfoView.as_view()),
#     path('book/<int:pk>', views.BookInfoView.as_view(), name='bk'),
#     path('page', views.PagerView.as_view()),
#
#     path('view', views.ViewView.as_view({'get': 'list', 'post': 'create'})),
#     path('view/<int:pk>', views.ViewView.as_view({'get': 'retrieve',
#                                                   'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
# ]
#
# urlpatterns += url_stydy

