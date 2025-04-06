from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
    path("checkout/", views.checkout, name="checkout"),
]