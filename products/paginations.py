from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    """Custom pagination class for the Product API views."""

    page_size_query_param = "limit"
    page_size = 10
    page_query_param = "currentPage"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        """Get the paginated response with additional pagination information."""
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )
