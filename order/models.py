from django.db import models
from account.models import User
from content.models import Product,Variant
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from conf.settings import EMAIL_HOST_USER
from django.core.mail import send_mail



class Order(models.Model):
    
    Payment_methods = [
        ("Cash On Delivery","Cash On Delivery")
    ]

    Status = [
        ('Pending','Pending'),
        ('Paid','Paid')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    payment_method = models.CharField(max_length=100,choices=Payment_methods,default="Cash On Delivery")
    status = models.CharField(max_length=100,choices=Status,default="Pending",null=True,blank=True)
    
    @property
    def total_price(self):
        order_products = OrderProduct.objects.filter(order__id=self.id)
        price_list = []
        for order_product in order_products:
            try:
                variant = Variant.objects.get(id=order_product.variant.id)
                price = variant.product.price * order_product.quantity
                price_list.append(price)
            except:
                pass
        total_price = sum(price_list)
        return total_price

class OrderProduct(models.Model):
    
    Choices = [
        ('S','Small'),
        ('M','Medium'),
        ('L','Large'),
        ('XL','Extra Large')
    ]
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_product')
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    
class Payment(models.Model):
    PAYMENT_STATUS = [
        ("Success","Success"),
        ("Pending","Pending"),
        ("Failed","Failed")
    ]

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=PAYMENT_STATUS,default="Pending")
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.IntegerField()

@receiver(post_save,sender=OrderProduct)
def post_save_order(sender,instance,created,**kwargs):
    variant = instance.variant
    variant.quantity -= instance.quantity
    variant.save()

      
@receiver(post_save,sender=Order)
def post_email_calculation(sender,instance,created,**kwargs):
    if created:
        user = instance.user
        email = user.email

        send_mail(
        "Your Order Has Been Created",
        f"You have ordered some clothes from MSGM Clothing and the order has been created.Thank You for shopping from MSGM Clothing and we hope you will like our services",
        EMAIL_HOST_USER,
        [email]
        )     
