from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.




class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    profile_pic=models.ImageField(null=True, blank=True)
    contact_no=models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    digital=models.BooleanField(default=False, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)
    image1=models.ImageField(null=True, blank=True)
    image2=models.ImageField(null=True, blank=True)
    image3=models.ImageField(null=True, blank=True)
    image4=models.ImageField(null=True, blank=True)

    description1=models.CharField(max_length=2550, default="", null=True, blank=True )
    description2=models.CharField(max_length=2550, default="")
    description3=models.CharField(max_length=2550, default="")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    user_name=models.CharField(max_length=200, default="blank")
    user_email=models.CharField(max_length=200, default="blank")
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True, blank=False)
    order_id=models.CharField(max_length=100, null=True)
    shipping_address=models.CharField(max_length=100, null=True)
    product_details=models.CharField(max_length=100, null=True)
    contact_no= models.CharField(max_length=12, null=True)

    
    @property
    def get_cart_total(self):
        orderitems=self.order_item_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.order_item_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class Order_Item(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    price=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

class MyOrder(models.Model):
    customer=models.CharField(max_length=200, null=False, default='None')
    customer_name=models.CharField(max_length=200, null=False, default='None')
    customer_email=models.CharField(max_length=200, null=False, default='None')
    name=models.CharField(max_length=200, null=False)
    price=models.FloatField()
    image=models.ImageField(null=True, blank=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    product_id=models.IntegerField(default=0)
    order_id=models.IntegerField(null=True, blank=True, default=0)
    shipping_address=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name