from rest_framework.pagination import PageNumberPagination


class CommunityPagination(PageNumberPagination):
    page_size = 20
