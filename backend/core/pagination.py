from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        return Response({
            "total_items": count,
            "total_pages": self.page.paginator.num_pages,
            "prev": bool(self.get_previous_link()),
            "next": bool(self.get_next_link()),
            "data": data
        })
