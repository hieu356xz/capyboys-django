from django.shortcuts import render
from django.db.models import Q
from home.utils import QueryParams
from product.models import Book
from blog.models import Blog
from .utils import get_queryset_with_filter

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

def index(request):
    new_products = Book.objects.all().order_by("-pk")[:10]
    best_selling_products = Book.objects.all()[:10] # Placeholder
    vietnamese_literatures = Book.objects.filter(collection__slug="van-hoc-viet-nam").order_by("-pk")[:10]
    manga_comics = Book.objects.filter(collection__slug="manga-comic").order_by("-pk")[:10]
    light_novels = Book.objects.filter(collection__slug="light-novel").order_by("-pk")[:10]
    new_blogs = Blog.objects.all().order_by("-publish_date")[:5]

    context = {
        "new_products": new_products,
        "best_selling_products": best_selling_products,
        "vietnamese_literatures": vietnamese_literatures,
        "manga_comics": manga_comics,
        "light_novels": light_novels,
        "new_blogs": new_blogs,
    }
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def search(request):
    PAGE_SIZE = 24
    query_params = QueryParams(request.GET, ("q", "page", "author", "genre", "price"))
    
    page = int(query_params.get('page', default=1))
    search_query = query_params.get("q", default="")
    author_query = query_params.get("author", default="")
    genre_query = query_params.get("genre", default="")
    price_query = query_params.get("price", default="")

    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE

    # queryset = Book.objects.all()

    # if collection_query: queryset = queryset.filter(collections__slug=collection_query)
    # if genre_query: queryset = queryset.filter(genres__name=genre_query)
    # if author_query: queryset = queryset.filter(authors__name=author_query)
    # if search_query: queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    queryset = Book.objects.none()

    queryset = get_queryset_with_filter(queryset, author_query, authors__name=author_query)
    queryset = get_queryset_with_filter(queryset, genre_query, genres__name=genre_query)
    queryset = get_queryset_with_filter(queryset, search_query, (Q(title__icontains=search_query) | Q(description__icontains=search_query)))

    if price_query and price_query in PRICE_RANGES:
        price_range = PRICE_RANGES[price_query]
        min_price = price_range["min_price"]
        max_price = price_range["max_price"]
        
        if min_price is not None and max_price is not None:
            queryset = get_queryset_with_filter(queryset, min_price, price__gte=min_price, price__lte=max_price)
        if min_price is not None:
            queryset = get_queryset_with_filter(queryset, min_price, price__gte=min_price)
        if max_price is not None:
            queryset = get_queryset_with_filter(queryset, max_price, price__lte=max_price)

    total_products = queryset.count()
    products = queryset[start:end]

    base_url = query_params.without("page").build_url('/search/')

    context = {
        "products": products,
        "total_products": total_products,
        "query": search_query,
        "base_url": base_url,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'home/search.html', context)

def handler404(request, exception):
    return render(request, 'home/404.html', status=404)