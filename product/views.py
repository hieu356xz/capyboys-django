from django.shortcuts import render
from django.http import Http404
from cart.cart import CartSession
from product.models import Book, BookAttributeValue

# Create your views here.
def product_detail(request, slug):
    try:
        cart = CartSession(request)
        product = Book.objects.get(slug=slug)
        product_attributes = BookAttributeValue.objects.filter(book=product).order_by('attribute__pk')
        collection = product.collections.first()
        formatted_price = f"{product.price:,.0f} ₫"
        authors = product.authors.all()
        max_quantity = max(0, min(product.stock - cart.get_item_quantity(product.pk), 99))
        min_quantity = 1 if max_quantity else 0
    except Book.DoesNotExist:
        raise Http404("Product does not exist")

    texmplate_name = 'product/product_detail.html'
    context = {
        "product": product,
        "collection": collection, 
        "product_price": formatted_price,
        "product_attributes": product_attributes,
        "authors": authors,
        "max_quantity": max_quantity,
        "min_quantity": min_quantity,
    }
    return render(request, texmplate_name, context)