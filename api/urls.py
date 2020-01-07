from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('subscriptions', views.SubscriptionViewSet)
router.register('product-types', views.ProductTypeViewSet)
router.register('products', views.ProductViewSet)
router.register('payment', views.PaymentViewSet)
router.register('payment-product', views.PaymentProductViewSet)
router.register('user-subscription', views.UsersSubscriptionsViewSet)
router.register('post', views.PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/', views.CustomRegisterView.as_view()),
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('train-constructor/', views.train_constructor, name='train_constructor')
]
