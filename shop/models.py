import datetime
from django.contrib.postgres.fields import ArrayField

from django.db import models


class ProductType(models.Model):
    type_name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.type_name)


class Product(models.Model):
    name = models.CharField(max_length=64)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    price = models.FloatField()
    weight = models.FloatField()
    portions = models.IntegerField()
    description = models.TextField(max_length=256, default=None)
    image = models.ImageField(upload_to="products")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Post(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def body(self):
        return self.text


class Order(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=256, null=True)
    state = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=256, null=True)
    zip_code = models.CharField(max_length=64, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


class Subscription(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    visits = models.PositiveIntegerField(default=12)
    visit_dates = ArrayField(models.DateField(), size=12, null=True, blank=True)
    is_active = models.BooleanField(default=True)


