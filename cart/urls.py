from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/", views.cart_add, name="add-to-cart"),
    path("view/", views.cart_modal_view, name="cart-modal"),
    path("remove/", views.cart_remove_item, name="remove-from-cart"),
    path("update/", views.cart_update_quantity, name="update-cart-item-qty"),
]
