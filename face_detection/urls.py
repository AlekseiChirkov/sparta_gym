from django.urls import path

from face_detection import views


urlpatterns = [
    path('detect/', views.detect)
]
