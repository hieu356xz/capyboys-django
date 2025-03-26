from django.shortcuts import render
from django.http import Http404
from collection.models import Collection
from product.models import Book

SORT_OPTIONS = {
    "newest": {
        "name": "Mới nhất",
        "order_by": "-id"
    },
    "oldest": {
        "name": "Cũ nhất",
        "order_by": "id"
    },
    "best-selling": {
        "name": "Bán chạy nhất",
        "order_by": "-id" # Placeholder
    },
    "title-ascending": {
        "name": "Tên A-Z",
        "order_by": "title"
    },
    "title-descending": {
        "name": "Tên Z-A",
        "order_by": "-title"
    },
    "price-ascending": {
        "name": "Giá thấp đến cao",
        "order_by": "price"
    },
    "price-descending": {
        "name": "Giá cao đến thấp",
        "order_by": "-price"
    }
}

def index(request, slug):
    PAGE_SIZE = 24
    page = int(request.GET.get('page', default=1))
    sort_key = request.GET.get('order', default='newest')

    if sort_key not in SORT_OPTIONS:
        sort_key = 'newest'

    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE
    
    collections = Collection.objects.all()

    if slug == 'all':
        current_collection = None
        queryset = Book.objects.all()
    else:
        try:
            current_collection = Collection.objects.get(slug=slug)
            queryset = current_collection.books.all()
        except Collection.DoesNotExist:
            raise Http404("Collection does not exist")
    
    sort_option = SORT_OPTIONS[sort_key]
    queryset = queryset.order_by(sort_option['order_by'])

    total_products = queryset.count()
    products = queryset[start:end]

    context = {
        "collections": collections,
        "current_collection": current_collection,
        "products": products,
        "sort_options": SORT_OPTIONS,
        "current_sort": sort_key,
        "slug": slug,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'collection/collection_base.html', context)
