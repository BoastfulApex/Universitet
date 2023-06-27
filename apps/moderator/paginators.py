from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil


class ApplicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = ceil(self.page.paginator.count / self.page_size)
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'results': data
        })
