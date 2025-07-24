from rest_framework import serializers
from content.serializer import VariantSerializer
from drf_writable_nested import WritableNestedModelSerializer
from .models import Order,OrderProduct,Payment,Feedback
from content.models import Product
from rest_framework.response import Response
from content.models import Variant


class OrderProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderProduct
        fields = ['id','order','variant','quantity']
        read_only_fields = ['order']

class OrderSerializer(WritableNestedModelSerializer):
    # total_price = serializers.SerializerMethodField()
    order_product = OrderProductSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id','user','order_product','country','city','address','phone_number','payment_method','status','total_price']
        read_only_fields = ['total_price']
    
    def validate(self,attrs):
        request = self.context.get('request')
        attrs['user'] = request.user
        order_product = attrs.get('order_product')
        
        if order_product is None:
            raise serializers.ValidationError({"error":"provide product you want to order"})
        
        for data in order_product:
            variant= data.get('variant')
            quantity = data.get('quantity')
            if variant is None:
                raise serializers.ValidationError({"error":"enter product's variant "})
            if quantity is None:
                raise serializers.ValidationError({"error":"enter cloth's quantity"})     
            if variant.quantity == 0:
                raise serializers.ValidationError({"error":"Sold Out"})
            if variant.quantity - quantity < 0:
                raise serializers.ValidationError({"error":"Insufficient stock"})
        
        return attrs 
        
class OrderListSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(many=True,read_only=True)
    
    class Meta:
        model = Order
        fields = ['id','user','order_product','country','city','address','phone_number','payment_method','status','total_price']
        read_only_fields = ['total_price']
class PaymentSerializer(serializers.ModelSerializer):
    total_price = total_price = serializers.ReadOnlyField(source='order.total_price')
    class Meta:
        model = Payment
        fields = ['id','order','amount_paid','total_price']

    def get_order_total_price(self, obj):
        return OrderSerializer(obj.order).data['total_price']
    
    def validate(self, attrs):
        order = attrs.get('order')
        total_price = order.total_price
        amount_paid = attrs.get('amount_paid')

        if order is None:
            raise serializers.ValidationError({"error":"provide the order id that you want to pay for "})
        if amount_paid is None:
            raise serializers.ValidationError({"error":"provide the payment"})
        if order.status == "Paid":
            raise serializers.ValidationError({"error":"this order was already paid"})
        if amount_paid < total_price or amount_paid > total_price:
            raise serializers.ValidationError({"error":f"you should pay {total_price}.Rs"})

        order.status = "Paid"
        order.save()
        return attrs   


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id','rating','comment','user']
    
    def validate(self, attrs):
        user = self.context.get('user')
        print('user',user)
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        return super().create(validated_data)
