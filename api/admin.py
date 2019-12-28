from django.contrib import admin
from django.contrib.auth.models import Group

from .forms import *
from .models import *


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(Payment)
admin.site.register(PaymentProduct)
