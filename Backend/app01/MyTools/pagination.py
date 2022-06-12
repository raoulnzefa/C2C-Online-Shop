# -*-coding:utf-8 -*-
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    def __init__(self, params):
        self.page_size = 20
        self.max_page_size = 100
        self.page_size_query_param = 'size'
        if params.get('size'):
            self.page_size = params['size']
