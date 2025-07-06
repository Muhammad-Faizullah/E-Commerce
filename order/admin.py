from django.contrib import admin
from .models import Order,Payment,OrderProduct

@admin.register(OrderProduct)
class OrderproductAdmin(admin.ModelAdmin):
    list_display = ['id','order','variant']
    list_per_page = 15
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','country','city','address']
    list_filter = ['country','city','status']
    search_fields = ['country','city','status']
    list_per_page = 15
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','order','amount_paid']
    list_per_page = 15