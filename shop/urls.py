from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('update-item/', views.update_item, name='update-item'),
    path('training-programs/', views.train_constructor, name='train_constructor'),
]
