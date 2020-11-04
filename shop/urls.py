from django.urls import path
from django.contrib.staticfiles.urls import static

from . import views
from sparta import settings

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('profile/cart/', views.cart, name='cart'),
    path('update-item/', views.update_item, name='update-item'),
    path('training-programs/', views.train_constructor, name='train_constructor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
