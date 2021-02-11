import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


class ProductType(models.Model):
    type_name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

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
    digital = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

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

    class Meta:
        verbose_name = 'Пост/Новость'
        verbose_name_plural = 'Посты/Новости'

    def __str__(self):
        return str(self.title)

    def body(self):
        return self.text


class PriceList(models.Model):
    TYPES = (
        ('Одноразовая тренировка', 'Одноразовая тренировка'),
        ('Тренировки с тренером', 'Тренировки с тренером'),
        ('Неделя с тренером', 'Неделя с тренером'),
        ('Самостоятельные тренировки', 'Самостоятельные тренировки')
    )
    training_type = models.CharField(choices=TYPES, max_length=64)
    price = models.IntegerField()
    description_1 = models.CharField(max_length=64, blank=True, null=True)
    description_2 = models.CharField(max_length=64, blank=True, null=True)
    description_3 = models.CharField(max_length=64, blank=True, null=True)
    description_4 = models.CharField(max_length=64, blank=True, null=True)
    description_5 = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'


class Order(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=256, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        print(orderitems)
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

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
    digital = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    zip_code = models.CharField(max_length=64, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return str(self.address)


def get_subscription_expired_date():
    return (datetime.datetime.now() + datetime.timedelta(30)).date()


class Subscription(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=get_subscription_expired_date)
    visits = models.PositiveIntegerField(default=12)
    visit_dates = ArrayField(models.DateField(), size=12, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        unique_together = ('customer', 'end_date',)
