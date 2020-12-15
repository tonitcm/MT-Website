from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #One to one relation means user can only have one customer
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=200, null=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY =(
        ('Abstract', 'Abstract'),
        ('Africa', 'Africa'),
    )

    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    images = models.ImageField(null=True, blank=True) #allows to puts images dont put in your STATIC FILE
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    @property #attribute rather than a method keeps things simples
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    STATUS =(
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL) #many to one relationship, customer can have multiple orders
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) #
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):

    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL) #a single order can have multiple order items
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAdress(models.Model):

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.adress

"""
To add this class to the database need to run another migration
python manage.py makemigrations : Preps database for migration
python manage.py migrate: added the table to the database

Many to one:
Gives a dropdown menu

Many to Many:
Gives multi-select option

on_delete options explained:

There are seven possible actions to take when such event occurs:

CASCADE: When the referenced object is deleted, also delete the objects that have references to it 
(when you remove a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE.

PROTECT: Forbid the deletion of the referenced object. 
To delete it you will have to delete all objects that reference it manually. SQL equivalent: RESTRICT.

RESTRICT: (introduced in Django 3.1) Similar behavior as PROTECT that matches SQL's RESTRICT more accurately. 
(See django documentation example)

SET_NULL: Set the reference to NULL (requires the field to be nullable). 
For instance, when you delete a User, you might want to keep the comments he posted on blog posts, 
but say it was posted by an anonymous (or deleted) user. SQL equivalent: SET NULL.

SET_DEFAULT: Set the default value. SQL equivalent: SET DEFAULT.

SET(...): Set a given value. This one is not part of the SQL standard and is entirely handled by Django.

DO_NOTHING: Probably a very bad idea since this would create integrity issues in your database 
(referencing an object that actually doesn't exist). SQL equivalent: NO ACTION. (2)

In most cases, CASCADE is the expected behaviour, but for every ForeignKey, 
you should always ask yourself what is the expected behaviour in this situation. 
PROTECT and SET_NULL are often useful. Setting CASCADE where it should not, 
can potentially delete all of your database in cascade, by simply deleting a single user.

Example:

ON-CASCADE: If Customer (ME) were to be deleted it would also delete its order because it no longer exists
SET_NULL: It will leave its order even though the user has been deleted
PROTECT: In order to delete customer you would have to delete its order first manually

"""

