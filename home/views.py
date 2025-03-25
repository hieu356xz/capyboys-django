from django.shortcuts import render
from django.db.models import Q
from product.models import Book

def index(request):
    new_products = Book.objects.all().order_by("-pk")[:10]
    best_selling_products = Book.objects.all()[:10]
    vietnamese_literatures = Book.objects.filter(collection__name="Văn học Việt Nam")[:10]
    manga_comics = Book.objects.filter(collection__name="Manga - Comic")[:10]
    light_novels = Book.objects.filter(collection__name="Light Novel")[:10]

    context = {
        "new_products": new_products,
        "best_selling_products": best_selling_products,
        "vietnamese_literatures": vietnamese_literatures,
        "manga_comics": manga_comics,
        "light_novels": light_novels
    }
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def search(request):
    PAGE_SIZE = 24
    query = request.GET.get("q")
    page = int(request.GET.get('page', default=1))
    print(page)

    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE

    filtered_books = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    total_products = filtered_books.count()
    products = filtered_books[start:end]

    context = {
        "products": products,
        "total_products": total_products,
        "query": query,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1
    }
    return render(request, 'home/search.html', context)

def handler404(request, exception):
    return render(request, 'home/404.html', status=404)