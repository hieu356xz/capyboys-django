from django.shortcuts import redirect, render
from django.db.models import Q, Subquery, Sum
from django.core.validators import validate_email
import phonenumbers
from cart.cart import CartSession
from cart.models import Order, OrderItem
from home.utils import QueryParams
from product.models import Author, Book, Genre
from blog.models import Blog

PRICE_RANGES = {
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

def index(request):
    new_products = Book.objects.all().order_by("-pk")[:10]
    best_selling_products = Book.objects.annotate(
            sale_count=Sum("orderitem__quantity", default=0)
        ).order_by("-sale_count", "-id")[:10]
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
    query_params = QueryParams(request.GET, ("q", "page", "author", "genre", "price", "order"))
    
    page = int(query_params.get('page', default=1))
    search_query = query_params.get("q", default="")
    author_query = query_params.get("author", default="")
    genre_query = query_params.get("genre", default="")
    price_query = query_params.get("price", default="")
    sort_key = query_params.get_if_not_in('order', SORT_OPTIONS, "newest")

    start = max((page - 1) * PAGE_SIZE, 0)
    end = start + PAGE_SIZE

    # queryset = Book.objects.all()

    # if collection_query: queryset = queryset.filter(collections__slug=collection_query)
    # if genre_query: queryset = queryset.filter(genres__name=genre_query)
    # if author_query: queryset = queryset.filter(authors__name=author_query)
    # if search_query: queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    filter_conditions = Q()
    
    if author_query:
        filter_conditions &= Q(authors__name=author_query)
    
    if genre_query:
        filter_conditions &= Q(genres__name=genre_query)
    
    if search_query:
        filter_conditions &= (Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if not filter_conditions:
        queryset = Book.objects.none()
    else:
        if price_query in PRICE_RANGES:
            price_range = PRICE_RANGES[price_query]
            min_price = price_range["min_price"]
            max_price = price_range["max_price"]

            if min_price and max_price:
                filter_conditions &= Q(price__gte=min_price, price__lte=max_price)
            elif min_price:
                filter_conditions &= Q(price__gte=min_price)
            elif max_price:
                filter_conditions &= Q(price__lte=max_price)

        queryset = Book.objects.filter(filter_conditions)

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

    base_url = query_params.without("page").build_url('/search/')

    context = {
        "products": products,
        "total_products": total_products,
        "query": search_query,
        "base_url": base_url,
        "sort_options": SORT_OPTIONS,
        "current_page": page,
        "total_page": total_products // PAGE_SIZE + 1,
        "related_authors": related_authors,
        "related_genres": related_genres,
        "price_ranges": PRICE_RANGES,
        "price_query": price_query,
        "author_query": author_query,
        "genre_query": genre_query,
    }
    return render(request, 'home/search.html', context)

def checkout(request):
    cart = CartSession(request)
    if cart.get_item_count() == 0:
        return redirect("cart")

    PAYMENT_METHODS = {
        "cod": "Thanh toán khi nhận hàng",
        "bank_transfer": "Chuyển khoản ngân hàng",
        "credit_card": "Thẻ tín dụng",
        "e_wallet": "Ví điện tử",
    }

    first_name = request.user.first_name if request.user.is_authenticated else ''
    last_name = request.user.last_name if request.user.is_authenticated else ''
    email = request.user.email if request.user.is_authenticated else ''
    phone = ''
    address = ''
    city = ''
    district = ''
    ward = ''
    notes = ''
    payment_method = ''
    errors = {}

    if request.method == "POST":
        if not request.user.is_authenticated:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        district = request.POST.get("district")
        ward = request.POST.get("ward")
        notes = request.POST.get("notes")
        payment_method = request.POST.get("payment_method")

        if not first_name:
            errors["first_name"] = "Vui lòng nhập tên"

        if not email:
            errors["email"] = "Vui lòng nhập email"
        else:
            try:
                validate_email(email)
            except Exception:
                errors["email"] = "Email không hợp lệ"
        
        if not phone:
            errors["phone"] = "Vui lòng nhập số điện thoại"
        else:
            try:
                parsed_phone = phonenumbers.parse(phone, "VN")
                if not phonenumbers.is_valid_number(parsed_phone):
                    errors["phone"] = "Số điện thoại không hợp lệ"
            except phonenumbers.NumberParseException:
                errors["phone"] = "Số điện thoại không hợp lệ"

        if not address:
            errors["address"] = "Vui lòng nhập địa chỉ"
        if not city:
            errors["city"] = "Vui lòng nhập tỉnh/thành phố"
        if not district:
            errors["district"] = "Vui lòng nhập quận/huyện"
        if not ward:
            errors["ward"] = "Vui lòng nhập phường/xã"

        if not errors:
            try:
                order = Order(
                    user=request.user if request.user.is_authenticated else None,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    district=district,
                    ward=ward,
                    notes=notes,
                    payment_method=payment_method,
                    payment_status=False,
                )
                order.save()

                for item in cart:
                    book = Book.objects.get(pk=item['id'])
                    order_item = OrderItem(
                        order=order,
                        book=book,
                        quantity=item['quantity'],
                        price=book.price,
                    )
                    order_item.save()

                cart.clear()

                return redirect("checkout_success")
            except Exception as e:
                print(str(e))

    context = {
        "payment_methods": PAYMENT_METHODS,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address": address,
        "city": city,
        "district": district,
        "ward": ward,
        "notes": notes,
        "payment_method": payment_method,
        "errors": errors,
    }

    return render(request, 'home/checkout.html', context)

def checkout_success(request):
    return render(request, 'home/checkout_success.html', {})

def handler404(request, exception):
    return render(request, 'home/404.html', status=404)
