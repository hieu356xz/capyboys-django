from django.shortcuts import render
from product.models import Book, BookAttributeValue

# Create your views here.
def product_detail(request, slug):
    product = Book.objects.get(slug=slug)
    product_attributes = BookAttributeValue.objects.filter(book=product).order_by('attribute__pk')
    collection = product.collections.first()
    formatted_price = f"{product.price:,.0f} ₫"
    authors = product.authors.all()

    texmplate_name = 'product/product_detail.html'
    context = {
        "product": product,
        "collection": collection,
        "product_price": formatted_price,
        "product_attributes": product_attributes,
        "authors": authors
    }
    return render(request, texmplate_name, context)