# -*-coding:utf-8 -*-
from app01 import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class FirstAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        # 认证失败时，给浏览器的返回头
        pass


class Authenticate(BaseAuthentication):
    def authenticate(self, request):
        token_param = request.query_params.get('token')
        token_body = request.data.get('token')
        if token_param:
            token = token_param
        elif token_body:
            token = token_body
        else:
            token = None
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed({'code': 0})
        return token_obj.user, token_obj
        # (request.user, request.auth)

    def authenticate_header(self, request):
        pass


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


