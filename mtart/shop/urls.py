from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('gallery/', views.gallery, name="gallery"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('cart/', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout")
]

