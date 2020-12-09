from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=200, null=True)
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
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS =(
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)


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

