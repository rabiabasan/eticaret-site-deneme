from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("kategori/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("urun/<slug:slug>/", views.product_detail, name="product_detail"),
    path("sepet/", views.cart_detail, name="cart_detail"),
    path("sepet/ekle/<int:product_id>/", views.cart_add, name="cart_add"),
    path("sepet/cikar/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("siparis/olustur/", views.order_create, name="order_create"),
    path("api/products/", views.ProductListAPI.as_view(), name="api_product_list"),
    path("api/products/<slug:slug>/", views.ProductDetailAPI.as_view(), name="api_product_detail"),
    path("api/categories/", views.CategoryListAPI.as_view(), name="api_category_list"),
    path("hava-durumu/", views.weather, name="weather"),
]