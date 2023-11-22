from typing import Dict

from django.db.models.query import QuerySet

from products.models import Product


def get_total_price_product(product, count) -> float:
    """Calculate the total price for a product based on its quantity."""
    if hasattr(product, "sale"):
        return product.sale.salePrice * count
    return product.price * count


def convert_filters_and_sort_params_product(query_params) -> Dict:
    """Convert query parameters into filter and sort options for the Product model."""
    return {
        "name": query_params.get("filter[name]", ""),
        "min_price": query_params.get("filter[minPrice]", 0),
        "max_price": query_params.get("filter[maxPrice]", 50000),
        "free_delivery": bool(
            query_params.get("filter[freeDelivery]", "false") == "true"
        ),
        "available": bool(query_params.get("filter[available]", "false") == "true"),
        "category": query_params.get("category", None),
        "tags": query_params.getlist("tags[]", []),
        "sort_by": query_params.get("sort", "date"),
        "sort_type": query_params.get("sortType", "dec"),
    }


def change_product_rating(product, reviews) -> None:
    """Change the rating of a product based on reviews."""
    rates = [review.rate for review in reviews]
    product.rating = sum(rates) / len(rates)
    product.save()


def change_product_count(product, count_to_subtract) -> None:
    """Change the count of a product by subtracting the specified amount."""
    product.count -= count_to_subtract
    product.save()


def get_basket_contents(request) -> QuerySet:
    """Get the contents of the user's shopping basket."""
    basket = request.session.get("basket")
    if basket:
        queryset = Product.objects.filter(
            id__in=(int(product_id) for product_id in basket.keys())
        )

        for product in queryset:
            product.count = basket[str(product.id)]["count"]

        return queryset
    return Product.objects.none()


def add_to_basket(request) -> QuerySet:
    """Add a product to the user's shopping basket."""
    product_id = str(request.data.get("id"))
    count = request.data.get("count", 1)

    if "basket" not in request.session:
        request.session["basket"] = {}
    basket = request.session["basket"]
    if product_id in basket:
        basket[product_id]["count"] += count
    else:
        basket[product_id] = {"count": count}

    request.session.modified = True

    return get_basket_contents(request=request)


def remove_from_basket(request) -> QuerySet:
    """Remove a product from the user's shopping basket."""
    product_id = str(request.data.get("id"))
    count = request.data.get("count", 1)

    if "basket" in request.session:
        basket = request.session["basket"]
        if product_id in basket:
            if count < basket[product_id]["count"]:
                basket[product_id]["count"] -= count
            else:
                del basket[product_id]
            request.session.modified = True

    return get_basket_contents(request=request)


def delete_basket(request) -> None:
    """Delete the user's shopping basket."""
    del request.session["basket"]
    request.session.modified = True
