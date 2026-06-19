from django.contrib import admin
from .models import Category, Product, Order, OrderItem



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "available"]
    list_filter = ["available", "category", "created_at"]
    list_editable = ["price", "stock", "available"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "city", "paid", "created_at"]
    list_filter = ["paid", "created_at"]
    inlines = [OrderItemInline]