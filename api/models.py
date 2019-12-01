from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta


class Subscription(models.Model):
    subscription_type = models.CharField(max_length=64)
    time = models.TimeField(default=None)
    price = models.FloatField()

    def __str__(self):
        return self.subscription_type


class ProductType(models.Model):
    type_name = models.CharField(max_length=64)

    def __str__(self):
        return self.type_name


class Product(models.Model):
    name = models.CharField(max_length=64)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(max_length=256, default=None)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, date_of_birth, password=None):
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name
        )
        user.set_password(password)
        user.save()
        return user

    def create_staff_user(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            name=name
        )
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            name="True"
        )
        user.staff = True
        user.admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=64, default=None)
    date_of_birth = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name']

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=datetime.now()+timedelta(days=30))

    def __str__(self):
        return str(self.subscription_type)


class PaymentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product)

    def get_cost(self):
        return self.product.price * self.count


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_it_open = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(PaymentProduct)

    def __str__(self):
        return str(self.user)

    def get_sum(self):
        return sum(item.get_cost() for item in self.products.all())
