from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=254, null=True)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=254, null=True)
    description = models.TextField(max_length=1000, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, null = True, blank = True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except: 
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=254, null=True)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return self.product.name

class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=254, null=False)
    city = models.CharField(max_length=254, null=False)
    state = models.CharField(max_length=254, null=False)
    zipcode = models.CharField(max_length=254, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
            return self.address

class Comment(models.Model):
    name = models.CharField(max_length=254, null=True)
    email = models.EmailField(max_length=254, null=True)
    body = models.TextField(max_length=254,null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('-comment_date',)

    def __str__(self):
            return '{} add a comment to {} product'.format(self.name, self.product)