from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField("Kategori Adı", max_length=100)
    slug = models.SlugField("URL Adı", max_length=120, unique=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Kategori",
    )
    name = models.CharField("Ürün Adı", max_length=200)
    slug = models.SlugField("URL Adı", max_length=220, unique=True)
    description = models.TextField("Açıklama", blank=True)
    price = models.DecimalField("Fiyat", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Stok", default=0)
    image = models.ImageField("Resim", upload_to="products/", blank=True, null=True)
    available = models.BooleanField("Satışta mı?", default=True)
    created_at = models.DateTimeField("Eklenme Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Kullanıcı",
    )
    first_name = models.CharField("Ad", max_length=50)
    last_name = models.CharField("Soyad", max_length=50)
    email = models.EmailField("E-posta", blank=True)
    address = models.CharField("Adres", max_length=250)
    city = models.CharField("Şehir", max_length=100)
    phone = models.CharField("Telefon", max_length=20)
    created_at = models.DateTimeField("Sipariş Tarihi", auto_now_add=True)
    paid = models.BooleanField("Ödendi mi?", default=False)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Sipariş #{self.id} - {self.first_name} {self.last_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Sipariş",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Ürün",
    )
    price = models.DecimalField("Fiyat", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Adet", default=1)

    class Meta:
        verbose_name = "Sipariş Kalemi"
        verbose_name_plural = "Sipariş Kalemleri"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity