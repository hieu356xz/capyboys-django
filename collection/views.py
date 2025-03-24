from django.shortcuts import render
from django.http import Http404
from collection.models import Collection
from product.models import Book

sort_options = [
    {
        "id": 1,
        "name": "Mới nhất",
    },
    {
        "id": 2,
        "name": "Cũ nhất",
    },
    {
        "id": 3,
        "name": "Bán chạy nhất",
    },
    {
        "id": 4,
        "name": "Tên A-Z",
    },
    {
        "id": 5,
        "name": "Tên Z-A",
    },
    {
        "id": 6,
        "name": "Giá tăng dần",
    },
    {
        "id": 7,
        "name": "Giá giảm dần",
    },
]

def index(request, slug):
    PRODUCT_PER_PAGE = 24
    offset = int(request.GET.get('page', default=1))

    start = max((offset - 1) * PRODUCT_PER_PAGE, 0)
    end = start + PRODUCT_PER_PAGE
    
    collections = Collection.objects.all()

    if slug == 'all':
        current_collection = None
        products = Book.objects.all()[start:end]
        total_products = Book.objects.count()
    else:
        try:
            current_collection = Collection.objects.get(slug=slug)
            products = current_collection.books.all()[start:end]
            total_products = current_collection.books.count()
        except Collection.DoesNotExist:
            raise Http404("Collection does not exist")
    
    context = {
        "collections": collections,
        "current_collection": current_collection,
        "products": products,
        "sort_options": sort_options,
        "slug": slug,
        "current_page": offset,
        "total_page": total_products // PRODUCT_PER_PAGE + 1
    }
    return render(request, 'collection/collection_base.html', context)
