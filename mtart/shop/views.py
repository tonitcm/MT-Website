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

    products = Product.objects.all()

    return render(request, "shop/gallery.html", {'products': products})

def cart(request):

    #for authenticator user, logged or not logged in
    if request.user.is_authenticated:
        customer = request.user.customer #one to one relationship
        order, created = Order.objects.get_or_create(customer=customer)#querying an object or creating one
        items = order.orderitem_set.all()
    else: #non-logged in user cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}

    return render(request, "shop/cart.html", context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer #one to one relationship
        order, created = Order.objects.get_or_create(customer=customer)#querying an object or creating one
        items = order.orderitem_set.all()
    else: #non-logged in user cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, "shop/checkout.html", context)


