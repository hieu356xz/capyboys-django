from django.shortcuts import render

from product.models import Book

def index(request):
    new_products = Book.objects.all().order_by("-pk")[:10]
    best_selling_products = Book.objects.all()[:10]
    vietnamese_literatures = Book.objects.filter(collection__name="Văn học Việt Nam")[:10]
    manga_comics = Book.objects.filter(collection__name="Manga - Comic")[:10]
    light_novels = Book.objects.filter(collection__name="Light Novel")[:10]

    print(new_products)
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