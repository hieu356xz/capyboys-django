from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.cart_add, name="add-to-cart"),
    path("view/", views.cart_modal_view, name="cart-modal")
]
