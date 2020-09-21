from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active', 'is_admin']
    list_display_links = ['id', 'email', 'username']

    class Meta:
        model = MyUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

    class Meta:
        model = Profile


class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]

    class Meta:
        model = Customer


admin.site.register(MyUser, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Customer, CustomerAdmin)
