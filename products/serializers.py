from rest_framework import serializers

from products.models import (Category, CategoryImage, Product, ProductImage,
                             ProductSale, Review, Specification, Tag)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for the ProductImage model."""

    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("src", "alt")

    def get_src(self, obj) -> str:
        """Get the URL of the image source."""
        return obj.src.url


class CategoryImageSerializer(serializers.ModelSerializer):
    """Serializer for the CategoryImage model."""

    src = serializers.SerializerMethodField()

    class Meta:
        model = CategoryImage
        fields = ("src", "alt")

    def get_src(self, obj) -> str:
        """Get the URL of the image source."""
        return obj.src.url


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_subcategories(self, obj):
        """Get the subcategories of the category."""
        queryset = Category.objects.filter(category=obj.pk)
        serializer = SubcategorySerializer(queryset, many=True)
        return serializer.data


class SubcategorySerializer(serializers.ModelSerializer):
    """Serializer for the Subcategory model."""

    image = CategoryImageSerializer()

    class Meta:
        model = Category
        exclude = ("category",)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    class Meta:
        model = Review
        exclude = (
            "id",
            "product",
            "profile",
        )

    def create(self, validated_data):
        """Create a review."""
        if validated_data.get("profile"):
            profile = validated_data["profile"]
            validated_data["author"] = profile.fullName
            validated_data["email"] = profile.user.email

        return super().create(validated_data)


class SpecificationSerializer(serializers.ModelSerializer):
    """Serializer for the Specification model."""

    class Meta:
        model = Specification
        exclude = ("id",)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta:
        model = Tag
        fields = "__all__"


class ProductShortSerializer(serializers.ModelSerializer):
    """Serializer for a short representation of the Product model."""

    price = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ("fullDescription", "specifications")

    def get_price(self, obj) -> float:
        """Get the price of the product, but first check if there is a discount"""
        if hasattr(obj, "sale"):
            return obj.sale.salePrice
        return obj.price


class ProductSerializer(ProductShortSerializer):
    """Serializer for the full representation of the Product model."""

    reviews = ReviewSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductSaleSerializer(serializers.ModelSerializer):
    """Serializer for the ProductSale model."""

    title = serializers.CharField(source="product.title", read_only=True)
    images = ProductImageSerializer(source="product.images", many=True, read_only=True)
    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = ProductSale
        fields = (
            "id",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "price",
            "images",
        )
