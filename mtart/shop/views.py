from django.shortcuts import render
from .models import *

def home(request):
    return render(request, "shop/home.html")

def customer(request, pk):

    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}


    return render(request, "shop/customer.html", context)

def about(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()

    context = {'customers': customers, 'total_orders': total_orders,

               }

    return render(request, "shop/about.html", context)

def gallery(request):
    return render(request, "shop/gallery.html")

def cart(request):
    return render(request, "shop/cart.html")

def checkout(request):
    return render(request, "shop/checkout.html")


