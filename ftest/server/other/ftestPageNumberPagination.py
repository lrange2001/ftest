from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.views import Response
class Mypageination(PageNumberPagination):
    page_size = 10 #默认每页显示多少条
    page_query_param = 'page_num' #指定查询的第几页 页码 默认page
    page_size_query_param = 'page_size' #指定每条显示多少条
    max_page_size = 50 #每页最多显示多少条
    def get_paginated_response(self, data):
        code = 200
        msg = '成功'
        if not data:
            code = 404
            msg = '没有发现数据'
        return Response(OrderedDict([
            ('code',code),
            ('message',msg),
            ('count', self.page.paginator.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('data', data)
        ]))
