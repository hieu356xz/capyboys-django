from django.shortcuts import render
from django.db.models import Q
from home.utils import QueryParams
from product.models import Book
from blog.models import Blog
from .utils import get_queryset_with_filter


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
    query_params = QueryParams(request.GET, ("q","page", "author", "genre"))
    
    page = int(query_params.get('page', default=1))
    search_query = query_params.get("q", default="")
    author_query = query_params.get("author", default="")
    genre_query = query_params.get("genre", default="")

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

    total_products = queryset.count()
    products = queryset[start:end]

    context = {
        "products": products,
        "total_products": total_products,
        "query": search_query,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'home/search.html', context)

def handler404(request, exception):
    return render(request, 'home/404.html', status=404)