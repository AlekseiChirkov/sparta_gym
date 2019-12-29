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


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=64, unique=True)
    username = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserSubscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_it_open = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(PaymentProduct)

    def __str__(self):
        return str(self.user)

    def get_sum(self):
        return sum(item.get_cost() for item in self.products.all())


class Post(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
