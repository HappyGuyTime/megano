from django.db.models import Count
from django.db.models.query import QuerySet
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products import serializers, services
from products.filters import ProductFilter
from products.models import Category, Product, ProductSale, Review, Tag
from products.paginations import ProductPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API provides read-only access to product information,
    including retrieving product details and filtered product lists.
    """

    serializer_class = serializers.ProductShortSerializer
    queryset = Product.objects.select_related("sale").all().order_by("-date")

    def retrieve(self, request, *args, **kwargs) -> Response:
        """Retrieve detailed information about a specific product."""
        instance = self.get_object()
        serializer = serializers.ProductSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, url_path="popular", methods=["get"])
    def popular(self, request) -> Response:
        """Retrieve a list of popular products based on the number of reviews."""
        queryset = self.queryset.annotate(reviews_count=Count("reviews")).order_by(
            "-reviews_count"
        )[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="limited", methods=["get"])
    def limited(self, request) -> Response:
        """Retrieve a list of products with limited availability based on the stock count."""
        queryset = self.queryset.order_by("count")[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="banners", methods=["get"])
    def banners(self, request) -> Response:
        """Retrieve a list of products to be displayed as banners."""
        queryset = self.queryset.order_by("?")[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductSaleListView(generics.ListAPIView):
    """API for receiving discounted products."""

    queryset = (
        ProductSale.objects.all()
        .select_related("product")
        .prefetch_related("product__images")
        .order_by("-salePrice")
    )
    serializer_class = serializers.ProductSaleSerializer
    pagination_class = ProductPagination


class CatalogAPIView(generics.ListAPIView):
    """API for browsing product catalog."""

    serializer_class = serializers.ProductShortSerializer
    pagination_class = ProductPagination
    filterset_class = ProductFilter
    queryset = Product.objects.select_related("sale").all()

    def get_queryset(self) -> QuerySet[Product]:
        """Get the queryset of products based on filtering and sorting parameters."""
        query_params = services.convert_filters_and_sort_params_product(
            query_params=self.request.GET
        )
        filterset = self.filterset_class(data=query_params, queryset=self.queryset)

        if filterset.is_valid():
            return filterset.qs
        return self.queryset


class ReviewApiView(generics.CreateAPIView):
    """API for creating and managing product reviews."""

    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        """Performs the creation of a review."""
        self.product = Product.objects.get(pk=self.kwargs.get("id"))
        serializer.save(product=self.product, profile=self.profile)

    def create(self, request, *args, **kwargs) -> Response:
        """Handles the creation of a new review."""
        self.profile = None

        if request.user.is_authenticated:
            self.profile = request.user.profile

        super().create(request, *args, **kwargs)
        reviews = Review.objects.filter(product=self.product)
        services.change_product_rating(product=self.product, reviews=reviews)
        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListView(generics.ListAPIView):
    """API for listing tags."""

    serializer_class = serializers.TagSerializer
    pagination_class = None
    queryset = Tag.objects.all()


class CategoryListView(generics.ListAPIView):
    """API for listing categories."""

    serializer_class = serializers.CategorySerializer
    pagination_class = None
    queryset = Category.objects.filter(category__isnull=True)


class BasketView(generics.GenericAPIView):
    """API for managing the user's basket."""

    serializer_class = serializers.ProductShortSerializer

    def get(self, request) -> Response:
        """Retrieve the contents of the user's basket."""
        queryset = services.get_basket_contents(request)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request) -> Response:
        """Add a product to the user's basket."""
        queryset = services.add_to_basket(request)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request) -> Response:
        """Remove a product from the user's basket."""
        queryset = services.remove_from_basket(request)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
