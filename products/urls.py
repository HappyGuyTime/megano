from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import (BasketView, CatalogAPIView, CategoryListView,
                            ProductSaleListView, ProductViewSet, ReviewApiView,
                            TagListView)

app_name = "products"

router = DefaultRouter()
router.register(r"products", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("popular/", ProductViewSet.as_view({"get": "popular"}), name="popular"),
    path("limited/", ProductViewSet.as_view({"get": "limited"}), name="limited"),
    path("products/<int:id>/reviews/", ReviewApiView.as_view(), name="review"),
    path("banners/", ProductViewSet.as_view({"get": "banners"}), name="banners"),
    path("sales/", ProductSaleListView.as_view(), name="sales"),
    path("catalog/", CatalogAPIView.as_view(), name="catalog"),
    path("tags/", TagListView.as_view(), name="tags"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("basket/", BasketView.as_view(), name="basket"),
]
