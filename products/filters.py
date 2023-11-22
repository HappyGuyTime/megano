import django_filters
from django.db.models import Case, Count, F, IntegerField, Q, When
from django.db.models.query import QuerySet

from products.models import Tag


class ProductFilter(django_filters.FilterSet):
    """FilterSet for filtering and sorting products."""

    name = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Product Name (Search)"
    )
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Minimum Price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Maximum Price"
    )
    free_delivery = django_filters.BooleanFilter(
        field_name="freeDelivery", label="Free Delivery"
    )
    available = django_filters.BooleanFilter(
        field_name="count", method="filter_available", label="Available in Stock"
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        to_field_name="id",
        queryset=Tag.objects.all(),
        conjoined=True,
        label="Tags",
    )
    category = django_filters.NumberFilter(
        field_name="category",
        lookup_expr="exact",
        method="filter_category",
        label="Category",
    )
    sort_by = django_filters.CharFilter(method="filter_sort", label="Sorting")

    def filter_available(self, queryset, name, value) -> QuerySet:
        """Filter by product availability."""
        if value:
            return queryset.filter(count__gt=0)
        return queryset

    def filter_category(self, queryset, name, value) -> QuerySet:
        """Filter by product category."""
        if value:
            return queryset.filter(Q(category_id=value) | Q(category__category_id=value))
        return queryset

    def filter_sort(self, queryset, name, value) -> QuerySet:
        """Sorts products by parameters"""
        if value == "reviews":
            queryset = queryset.annotate(reviews_count=Count("reviews"))
            value = "reviews_count"

        if value == "price":
            queryset = queryset.annotate(
                final_price=Case(
                    When(sale__salePrice__isnull=False, then=F("sale__salePrice")),
                    default=F("price"),
                    output_field=IntegerField(),
                )
            )
            value = "final_price"

        if self.data["sort_type"] == "inc":
            return queryset.order_by(F(value).asc(nulls_last=True))
        return queryset.order_by(F(value).desc(nulls_last=True))
