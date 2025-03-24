from django.urls import path
from . import views

urlpatterns = [
    path("<str:blog_type_slug>/", views.blog_list, name="blog_list"),
    path("<str:blog_type_slug>/<str:blog_slug>/", views.blog_detail, name="blog_detail"),
]
