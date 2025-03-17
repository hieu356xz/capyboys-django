from django.urls import path
from . import views

urlpatterns = [
    # path("<str:slug>/", views.product_detail, name="product_detail"),
    path("", views.index)
]