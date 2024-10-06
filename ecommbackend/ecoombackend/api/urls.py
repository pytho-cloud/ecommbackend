from django.contrib import admin
from django.urls import path ,include
from .views import *

from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/products/", ProductAPIView.as_view()), 
    path("api/products-home/", HomeProductView.as_view()),

    path("api/products/<str:pk>/", ProductAPIView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>', VerifyEmailView.as_view(), name='verify_email'),
    path('login/',LoginView.as_view(),name = "login"),
     path('user/get_user_details/',UserDataApiView.as_view(),name = "get_user_details"),
      path('user/get_user_address/',UserDataForAddressApiView.as_view(),name = "get_user_address"),
      path('user/add_user_wish_list/',SaveWishListView.as_view(),name = "add_user_wish_list"),
       path('user/add_user_wish_list/<str:pk>', SaveWishListView.as_view(), name="add_user_wish_list_with_pk"),
        path('user/delete_user_wish_list/<str:pk>/', SaveWishListView.as_view(), name="delete_user_wish_list"),
        path('user/user_checkout/<str:pk>/', CheckoutView.as_view(), name="user_checkout"),

]
