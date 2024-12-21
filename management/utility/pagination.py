from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class Pagination(PageNumberPagination):
    page_size = getattr(settings, 'PAGINATION_PAGE_SIZE', 2)
