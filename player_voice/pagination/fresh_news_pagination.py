from rest_framework.pagination import PageNumberPagination

class FreshNewsPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None
