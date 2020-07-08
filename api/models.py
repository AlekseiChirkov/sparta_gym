from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class ProductType(models.Model):
    type_name = models.CharField(max_length=64)

    def __str__(self):
        return self.type_name


class Product(models.Model):
    name = models.CharField(max_length=64)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(max_length=256, default=None)
    image = models.ImageField(upload_to="products")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

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


class Customer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=64, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=256, null=True)
    state = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=256, null=True)
    zip_code = models.CharField(max_length=64, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
