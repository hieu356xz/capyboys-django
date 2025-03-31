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
                            "total_quantity": cart.get_item_quantity(product_id),
                            "total_cart_item": cart.get_item_count(),
                        }
                    }, status=200)
                else:
                    return JsonResponse(data = {
                        "status": 400,
                        "message": f"Sản phẩm {product.title} thêm vào giỏ hàng thất bại. Số lượng hàng trong kho không đủ. Nếu bạn có nhu cầu đặt thêm xin hãy liên hệ với chúng tôi.",
                        "data": {
                            "product_id": product_id,
                            "product_title": product.title,
                            "added_quantity": quantity,
                            "total_quantity": cart.get_item_quantity(product_id),
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
        except Exception as e:
            return JsonResponse(data = {
                "status": 400,
                "message": f"Yêu cầu không hợp lệ: {str(e)}",
            }, status=400)

def cart_update_quantity(request):
    if request.method == "POST":
        try:
            cart = Cart(request)
            product_id = int(request.POST.get("product_id"))
            quantity = int(request.POST.get("quantity"))
            add_success, product = cart.update_quantity(product_id, quantity)
            if product:
                if add_success: 
                    return JsonResponse(data = {
                        "status": 200,
                        "message": f"Sản phẩm {product.title} được thêm vào giỏ hàng thành công",
                        "data": {
                            "product_id": product_id,
                            "product_title": product.title,
                            "total_quantity": cart.get_item_quantity(product_id),
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
                            "total_quantity": cart.get_item_quantity(product_id),
                        }
                    }, status=400)
            else:
                return JsonResponse(data = {
                    "status": 404,
                    "message": f"Sản phẩm không tồn tại trong giỏ hàng của bạn",
                    "data": {
                        "product_id": product_id,
                        "quantity": quantity,
                    }
                }, status=404)
        except Exception as e:
            return JsonResponse(data = {
                "status": 400,
                "message": f"Yêu cầu không hợp lệ: {str(e)}",
            }, status=400)

def cart_remove_item(request):
    if request.method == "POST":
        try:
            cart = Cart(request)
            product_id = int(request.POST.get("product_id"))

            remove_success = cart.remove(product_id)

            if remove_success:
                return JsonResponse(data = {
                    "status": 200,
                    "message": "Sản phẩm đã được xóa khỏi giỏ hàng",
                    "data": {
                        "product_id": product_id,
                        "total_cart_item": cart.get_item_count(),
                    }
                }, status=200)
            else:
                return JsonResponse(data = {
                    "status": 404,
                    "message": "Sản phẩm không tồn tại trong giỏ hàng của bạn",
                    "data": {
                        "product_id": product_id,
                    }
                }, status=404)
        except Exception as e:
            return JsonResponse(data = {
                "status": 400,
                "message": f"Yêu cầu không hợp lệ: {str(e)}",
            }, status=400)


def cart_modal_view(request):
    return render(request, "includes/cart_modal.html")

