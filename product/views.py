from django.shortcuts import render
from django.http import Http404
from cart.cart import CartSession
from product.models import Book, BookAttributeValue

# exclude general collections
exclude_collections = (
    "lich-su-truyen-thong",
    "van-hoc-viet-nam",
    "truyen-tranh",
    "manga-comic",
    "light-novel",
    "kien-thuc-khoa-hoc",
)

def product_detail(request, slug):
    try:
        cart = CartSession(request)
        product = Book.objects.select_related('publisher').prefetch_related(
            'collections',
            'authors',
            'genres',
            'bookattributevalue_set'
        ).get(slug=slug)
        
        product_attributes = product.bookattributevalue_set.all()
        current_collection = product.collections.filter(slug=slug).first()
        collections = product.collections.exclude(slug__in=exclude_collections)
        authors = product.authors.all()
        genres = product.genres.all()

        related_products = Book.objects.filter(authors__in=authors).exclude(pk=product.id).distinct()
        related_genre_products = Book.objects.filter(genres__in=genres).exclude(pk=product.id).distinct()

        formatted_price = f"{product.price:,.0f} ₫"
        max_quantity = max(0, min(product.stock - cart.get_item_quantity(product.pk), 99))
        min_quantity = 1 if max_quantity else 0

    except Book.DoesNotExist:
        raise Http404("Product does not exist")

    texmplate_name = 'product/product_detail.html'
    context = {
        "product": product,
        "current_collection": current_collection,
        "collections": collections,
        "product_price": formatted_price,
        "product_attributes": product_attributes,
        "authors": authors,
        'genres': genres,
        "max_quantity": max_quantity,
        "min_quantity": min_quantity,
        "related_products": related_products,
        "related_genre_products": related_genre_products,
    }

    return render(request, texmplate_name, context)