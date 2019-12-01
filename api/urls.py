from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('subscriptions', views.SubscriptionViewSet)
router.register('product-types', views.ProductTypeViewSet)
router.register('products', views.ProductViewSet)
router.register('roles', views.RoleViewSet)
router.register('payment', views.PaymentViewSet)
router.register('payment-product', views.PaymentProductViewSet)
router.register('user-subscription', views.UsersSubscriptionsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/', views.CustomRegisterView.as_view()),
    path('', views.home, name='home'),
]
