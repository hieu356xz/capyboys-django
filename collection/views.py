from django.shortcuts import render
from django.http import Http404
from collection.models import Collection
from product.models import Book
from home.utils import QueryParams

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
    query_params = QueryParams(request.GET, ("order","page"))

    page = int(query_params.get('page', default=1))
    sort_key = query_params.get_if_not_in('order', SORT_OPTIONS, "newest")
    
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

    base_url = query_params.without("page").build_url(f"/collections/{slug}/")

    context = {
        "collections": collections,
        "current_collection": current_collection,
        "products": products,
        "sort_options": SORT_OPTIONS,
        "current_sort": sort_key,
        "base_url": base_url,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'collection/collection_base.html', context)
