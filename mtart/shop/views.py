from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *

def home(request):
    return render(request, "shop/home.html")

def customer(request):

    customer = Customer.objects.get()
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

    if request.user.is_authenticated:
        customer = request.user.customer  # one to one relationship
        order, created = Order.objects.get_or_create(customer=customer)  # querying an object or creating one
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:  # non-logged in user cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, "shop/gallery.html", context)


def cart(request):

#checks if it is a logged in user or not

    if request.user.is_authenticated:
        customer = request.user.customer  # one to one relationship
        order, created = Order.objects.get_or_create(customer=customer)  # querying an object or creating one
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:  # non-logged in user cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, "shop/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer  # one to one relationship
        order, created = Order.objects.get_or_create(customer=customer)  # querying an object or creating one
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:  # non-logged in user cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, "shop/checkout.html", context)

def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action) #prints out the action "add"
    print('productId', productId) #prints out the productId

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) #change the quantity of the order item

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data', request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        # to prevent manipulation of data, check if total that is passed in is the same as cart total
        if total == order.get_cart_total:
            order.complete = True
        order.save()

    else:
        print('User is not logged in')




    return JsonResponse('Payment complete', safe=False)

