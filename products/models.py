from django.db import models

from profiles.models import Profile


class Product(models.Model):
    """Model representing a product."""

    title = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=300, null=False, blank=True)
    fullDescription = models.TextField(max_length=500, null=False, blank=True)
    freeDelivery = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    tags = models.ManyToManyField("Tag", related_name="products")
    specifications = models.ManyToManyField("Specification", related_name="products")
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )

    class Meta:
        db_table = "products"

    def __str__(self) -> str:
        """Return a string representation of the product."""
        return self.title

    def save(self, *args, **kwargs) -> None:
        """Custom save method to ensure a default image is created if none exists."""
        super().save(*args, **kwargs)

        if not self.images.exists():
            ProductImage.objects.create(product=self, alt="default image")


class ProductSale(models.Model):
    """Model representing a product sale."""

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="sale")
    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    dateFrom = models.CharField(max_length=5)
    dateTo = models.CharField(max_length=5)

    class Meta:
        db_table = "products_sales"


class Review(models.Model):
    """Model representing a product review."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    author = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)
    text = models.TextField(max_length=500)
    rate = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products_reviews"

    def __str__(self) -> str:
        """Return a string representation of the review's author."""
        return self.author


class Specification(models.Model):
    """Model representing a product specification."""

    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        db_table = "specifications"

    def __str__(self) -> str:
        """Return a string representation of the specification."""
        return f"{self.name}: {self.value}"


class Tag(models.Model):
    """Model representing a product tag."""

    name = models.CharField(max_length=128)

    class Meta:
        db_table = "tags"

    def __str__(self) -> str:
        """Return a string representation of the tag."""
        return self.name


class Category(models.Model):
    """Model representing a product category."""

    title = models.CharField(max_length=128)
    category = models.ForeignKey(
        "self", null=True, related_name="subcategory", on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "products_categories"

    def __str__(self) -> str:
        """Return a string representation of the category."""
        return self.title

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        """Custom save method to ensure a default image is created if none exists."""
        super().save(force_insert, force_update, using, update_fields)

        if not hasattr(self, "image"):
            CategoryImage.objects.create(category=self, alt="default image")


def get_product_image_directory_path(instance: Product, filename: str) -> str:
    """Return the directory path for product images."""
    return f"products/images/product_{instance.pk}/{filename}"


def get_category_image_directory_path(instance: Category, filename: str) -> str:
    """Return the directory path for category images."""
    return f"categories/images/category_{instance.pk}/{filename}"


class ProductImage(models.Model):
    """Model representing an image for a product."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(
        upload_to=get_product_image_directory_path,
        default="products/images/default.png",
    )
    alt = models.CharField(max_length=128)

    class Meta:
        db_table = "products_images"


class CategoryImage(models.Model):
    """Model representing an image for a product category."""

    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="image"
    )
    src = models.ImageField(
        upload_to=get_category_image_directory_path,
        default="categories/images/default.png",
    )
    alt = models.CharField(max_length=128)

    class Meta:
        db_table = "products_category_images"
