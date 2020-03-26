from django.conf.urls import url
from django.urls import path, include
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
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('user/', views.CustomRegisterView.as_view()),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('train-constructor/', views.train_constructor, name='train_constructor'),
]
