from django.shortcuts import render
from django.http import JsonResponse
from product.models import Book
from .cart import Cart


def cart_add(request):
    if request.method == "POST":
        try:
            cart = Cart(request)
            product_id = int(request.POST.get("product_id"))
            quantity = int(request.POST.get("quantity"))
            product = Book.objects.get(pk=product_id)

            if product:
                add_success = cart.add(product, quantity)
                if add_success: 
                    return JsonResponse(data = {
                        "status": 200,
                        "message": f"Sản phẩm {product.title} được thêm vào giỏ hàng thành công",
                        "data": {
                            "product_id": product_id,
                            "product_title": product.title,
                            "added_quantity": quantity,
                            "total_quantity": cart.get_subtotal(product_id),
                            "total_cart_item": cart.get_item_count(),
                        }
                    }, status=200)
                else:
                    return JsonResponse(data = {
                        "status": 400,
                        "message": f"Sản phẩm {product.title} thêm vào giỏ hàng thất bại. Số lượng bạn đang đặt không thể lớn hơn số lượng còn lại trong kho. (còn lại {product.stock})",
                        "data": {
                            "product_id": product_id,
                            "product_title": product.title,
                            "added_quantity": quantity,
                            "total_quantity": cart.get_subtotal(product_id),
                            "stock": product.stock,
                            "total_cart_item": cart.get_item_count(),
                        }
                    }, status=400)
            else:
                return JsonResponse(data = {
                    "status": 404,
                    "message": f"Sản phẩm không tồn tại",
                    "data": {
                        "product_id": product_id,
                        "quantity": quantity,
                    }
                }, status=404)
        except Exception:
            return JsonResponse(data = {
                "status": 400,
                "message": "Yêu cầu không hợp lệ",
            }, status=400)
            

