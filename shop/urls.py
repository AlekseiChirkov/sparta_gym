from django.urls import path, include
from django.contrib.staticfiles.urls import static
from rest_framework import routers

from . import views
from users import views as user_views
from sparta import settings

app_name = 'shop'

router = routers.DefaultRouter()
router.register('subscription', views.SubscriptionViewSet)
router.register('users', user_views.UserViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('profile/cart/', views.cart, name='cart'),
    path('subscription-check/', views.subscription_check, name='subscription-check'),
    path('api/', include(router.urls)),
    path('update-item/', views.update_item, name='update-item'),
    path('training-programs/', views.train_constructor, name='train_constructor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
