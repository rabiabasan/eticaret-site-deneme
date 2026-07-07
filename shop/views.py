from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import OrderCreateForm
from rest_framework import generics
from .serializers import ProductSerializer, CategorySerializer
import requests
from decouple import config

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    context = {
        "categories": categories,
        "products": products,
        "current_category": current_category,
    }
    return render(request, "shop/product_list.html", context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        "product": product,
    }
    return render(request, "shop/product_detail.html", context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect("shop:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})

@login_required
def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("shop:product_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            return render(request, "shop/order_created.html", {"order": order})
    else:
        form = OrderCreateForm()

    return render(request, "shop/order_create.html", {"cart": cart, "form": form})


# ===== API VIEW'LERİ =====

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"


class CategoryListAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    

def weather(request):
    city = request.GET.get("city", "Ankara")  # varsayılan: Ankara
    api_key = config("WEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",   # Celsius için
        "lang": "tr",        # Türkçe açıklama
    }

    weather_data = None
    error = None

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "icon": data["weather"][0]["icon"],
            }
        elif response.status_code == 404:
            error = "Şehir bulunamadı."
        else:
            error = "Hava durumu alınamadı. (Anahtar henüz aktif olmayabilir.)"
    except requests.RequestException:
        error = "Bağlantı hatası oluştu."

    context = {
        "weather_data": weather_data,
        "error": error,
        "city": city,
    }
    return render(request, "shop/weather.html", context)