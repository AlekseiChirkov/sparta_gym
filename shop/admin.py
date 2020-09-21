from django.contrib import admin

from shop.models import *


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductType._meta.fields]

    class Meta:
        model = ProductType


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

    class Meta:
        model = Product


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]

    class Meta:
        model = Post


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

    class Meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderItem._meta.fields]

    class Meta:
        model = OrderItem


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShippingAddress._meta.fields]

    class Meta:
        model = ShippingAddress


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)


