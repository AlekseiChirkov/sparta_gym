from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(Payment)
admin.site.register(PaymentProduct)
admin.site.register(Role)
