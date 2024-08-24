from django.contrib import admin
from django.urls import path ,include
from .views import *
from .views import ProductAPIView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",index),
 
    path("api/products/", ProductAPIView.as_view()), 
    path("api/products/<str:pk>/", ProductAPIView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>', VerifyEmailView.as_view(), name='verify_email'),
    path('login/',LoginView.as_view(),name = "login")
]
