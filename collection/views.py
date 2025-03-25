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
    PAGE_SIZE = 24
    page = int(request.GET.get('page', default=1))

    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE
    
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
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'collection/collection_base.html', context)
