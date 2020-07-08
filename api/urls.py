from django.urls import path, include
from django.conf.urls import url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework import routers

from . import views
from sparta import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('train-constructor/', views.train_constructor, name='train_constructor'),
    path('shop/', views.shop, name='shop')
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
