from django.shortcuts import render
from django.db.models import Q, Subquery, Sum
from django.http import Http404
from collection.models import Collection
from product.models import Author, Book, Genre
from home.utils import QueryParams

PRICE_RANGES = {
    "all": {
        "name": "Tất cả",
        "min_price": None,
        "max_price": None,
    },
    "0-50000": {
        "name": "Nhỏ hơn 50.000đ",
        "min_price": 0,
        "max_price": 50000,
    },
    "50000-100000": {
        "name": "Từ 50.000đ đến 100.000đ",
        "min_price": 50000,
        "max_price": 100000,
    },
    "100000-200000": {
        "name": "Từ 100.000đ đến 200.000đ",
        "min_price": 100000,
        "max_price": 200000,
    },
    "200000-300000": {
        "name": "Từ 200.000đ đến 300.000đ",
        "min_price": 200000,
        "max_price": 300000,
    },
    "300000-400000": {
        "name": "Từ 300.000đ đến 400.000đ",
        "min_price": 300000,
        "max_price": 400000,
    },
    "400000-500000": {
        "name": "Từ 400.000đ đến 500.000đ",
        "min_price": 400000,
        "max_price": 500000,
    },
    "500000-max": {
        "name": "Lớn hơn 500.000đ",
        "min_price": 500000,
        "max_price": None,
    },
}

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
        "order_by": None # Will be handled in the view
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

general_collections = (
    "lich-su-truyen-thong",
    "van-hoc-viet-nam",
    "truyen-tranh",
    "manga-comic",
    "light-novel",
    "kien-thuc-khoa-hoc",
)

def index(request, slug):
    PAGE_SIZE = 24
    query_params = QueryParams(request.GET, ("page", "author", "genre", "price", "order"))

    page = int(query_params.get('page', default=1))
    author_query = query_params.get("author", default="")
    genre_query = query_params.get("genre", default="")
    price_query = query_params.get("price", default="")
    sort_key = query_params.get_if_not_in('order', SORT_OPTIONS, "newest")
    
    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE

    filter_conditions = Q()
    
    if author_query:
        filter_conditions &= Q(authors__name=author_query)
    
    if genre_query:
        filter_conditions &= Q(genres__name=genre_query)

    if price_query and price_query in PRICE_RANGES:
        price_range = PRICE_RANGES[price_query]
        min_price = price_range["min_price"]
        max_price = price_range["max_price"]
        
        if min_price and max_price:
            filter_conditions &= Q(price__gte=min_price, price__lte=max_price)
        elif min_price:
            filter_conditions &= Q(price__gte=min_price)
        elif max_price:
            filter_conditions &= Q(price__lte=max_price)
    else:
        price_query = "all"
    
    collections = Collection.objects.filter(slug__in=general_collections)

    if slug == 'all':
        current_collection = None
        queryset = Book.objects.filter(filter_conditions)
    else:
        try:
            current_collection = Collection.objects.get(slug=slug)
            queryset = current_collection.books.filter(filter_conditions)
        except Collection.DoesNotExist:
            raise Http404("Collection does not exist")

    if sort_key == "best-selling":
        queryset = queryset.annotate(
            sale_count=Sum("orderitem__quantity", default=0)
        ).order_by("-sale_count", "-id")
    else:
        sort_option = SORT_OPTIONS[sort_key]
        queryset = queryset.order_by(sort_option['order_by'])

    total_products = queryset.count()
    products = queryset[start:end]

    queryset = queryset.prefetch_related('authors', 'genres')

    related_authors = Author.objects.filter(
        id__in=Subquery(queryset.values('authors__id').distinct())
    )[:30]
    selected_authors = Author.objects.filter(name=author_query)
    related_authors = related_authors | selected_authors

    related_genres = Genre.objects.filter(
        id__in=Subquery(queryset.values('genres__id').distinct())
    )[:30]
    selected_genres = Genre.objects.filter(name=genre_query)
    related_genres = related_genres | selected_genres

    base_url = query_params.without("page").build_url(f"/collections/{slug}/")

    context = {
        "collections": collections,
        "current_collection": current_collection,
        "products": products,
        "sort_options": SORT_OPTIONS,
        "current_sort": sort_key,
        "base_url": base_url,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1,
        "related_authors": related_authors,
        "related_genres": related_genres,
        "price_ranges": PRICE_RANGES,
        "price_query": price_query,
        "author_query": author_query,
        "genre_query": genre_query,
    }
    return render(request, 'collection/collection_base.html', context)
