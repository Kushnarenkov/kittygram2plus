from rest_framework.pagination import PageNumberPagination

from .models import Cat

class CatsPagination(PageNumberPagination):
    page_size = 20
