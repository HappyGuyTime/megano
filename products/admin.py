from django.contrib import admin
from django.utils.html import format_html

from products.models import (Category, CategoryImage, Product, ProductImage,
                             ProductSale, Review, Specification, Tag)


class ProductSaleInline(admin.TabularInline):
    """Inline admin panel for ProductSale in the ProductAdmin."""

    model = ProductSale
    extra = 0


class ProductImageInline(admin.TabularInline):
    """Inline admin panel for ProductImage in the ProductAdmin."""

    model = ProductImage
    extra = 0
    fields = (
        "preview",
        "src",
        "alt",
    )
    readonly_fields = ("preview",)

    def preview(self, instance):
        """Generate an HTML preview of the image."""
        if instance.src:
            return format_html(
                f'<img src="{instance.src.url}" alt="{instance.alt}" width="150" />'
            )
        return "No Image"

    preview.short_description = "Preview"


class ReviewInline(admin.StackedInline):
    """Inline admin panel for Review in the ProductAdmin."""

    model = Review
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin panel for Product model."""

    inlines = (
        ProductSaleInline,
        ProductImageInline,
        ReviewInline,
    )
    list_display = (
        "title",
        "price",
        "count",
        "date",
        "rating",
    )
    list_filter = (
        "freeDelivery",
        "rating",
    )
    search_fields = (
        "title",
        "description",
        "fullDescription",
    )
    readonly_fields = (
        "date",
        "rating",
    )
    filter_horizontal = (
        "tags",
        "specifications",
    )
    date_hierarchy = "date"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "price",
                    "count",
                    "rating",
                    "date",
                    "freeDelivery",
                )
            },
        ),
        (
            "Description",
            {
                "fields": (
                    "description",
                    "fullDescription",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "category",
                    "tags",
                    "specifications",
                )
            },
        ),
    )


class CategoryImageInline(admin.TabularInline):
    """Inline admin panel for CategoryImage in the CategoryAdmin."""

    model = CategoryImage
    extra = 0
    fields = (
        "preview",
        "src",
        "alt",
    )
    readonly_fields = ("preview",)

    def preview(self, instance):
        """Generate an HTML preview of the image."""
        if instance.src:
            return format_html(
                f'<img src="{instance.src.url}" alt="{instance.alt}" width="150" />'
            )
        return "No Image"

    preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin class for managing Category objects."""

    inlines = (CategoryImageInline,)
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """Admin class for managing Specification objects."""

    list_display = ("name", "value")
    search_fields = ("name", "value")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin class for managing Tag objects."""

    list_display = ("name",)
    search_fields = ("name",)
