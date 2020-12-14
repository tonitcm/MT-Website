from django.contrib import admin
from .models import *

#GO TO HERE TO PUT THE MODEL CLASSES INSIDE THE ADMIN TO VISUALIZE

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)
