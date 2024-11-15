from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination.
    This class allows clients to define the page size via a query parameter.
    Attributes:
    page_size_query_param (str): The name of the query parameter used by clients
    to set the number of items per page. By default,
    this is set to "size".
    """

    page_size_query_param = "size"
