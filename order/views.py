
from django.shortcuts import render
from content.models import Product
from .models import Order,Feedback
from .serializer import OrderSerializer,OrderListSerializer,PaymentSerializer,FeedbackSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.core.files.storage import Storage,default_storage,DefaultStorage
from content.filters import CategoryFilter,ProductFilter
from django_filters import rest_framework as filters
from account.permissions import AdminPermission,OwnerPermission
from rest_framework import viewsets
from .task import birthday_reminder
from django_celery_beat.models import IntervalSchedule,PeriodicTask
import json
# Create your views here.

class OrderView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def order_product(self,request):
        serializer = OrderSerializer(data=request.data,context={"request":request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
class OrderListView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def order_list(self,request):
        user = request.user
        print("user --- ",user)
        if user.is_admin is True or user.is_owner is True:
            obj = Order.objects.all().order_by("-id")
            serializer = OrderListSerializer(obj,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK) 
        obj = Order.objects.filter(user__id=user.id).order_by("-id")
        serializer = OrderListSerializer(obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   

# class OrderListView(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated] 

#     def order_list(self,request):
#         obj = Order.objects.all().order_by("-id")
#         serializer = OrderListSerializer(obj,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK) 
class PaymentView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def payment(self,request):
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"payment was successful"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TaskView(viewsets.ViewSet):
    
    def name_date(self,request,*args,**kwargs):
        birthday_reminder.delay(name="Sidique",date="21/06/2025")
        return Response({"Message":"Task stated"})
             
    def reminder(self,request,*args,**kwargs):
        
        interval, _ = IntervalSchedule.objects.get_or_create(
            every = 8,
            period = IntervalSchedule.SECONDS
        )
        PeriodicTask.objects.create(
            task = "order.task.birthday_reminder",
            interval = interval,
            name = "birthday reminder task"
        )
        return Response({"Message":"Task scheduled!"})

class FeedbackView(ListAPIView,CreateAPIView):
    queryset = Feedback.objects.all().order_by('-submitted_at')
    serializer_class = FeedbackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [] 

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [] 
        return [IsAdminUser()] 
    
    def post(self,request,*args,**kwargs):
        serializer = FeedbackSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class FeedbackViewForAdmin(ListAPIView,RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all().order_by('-submitted_at')
    serializer_class = FeedbackSerializer
    authentication_classes = []
    permission_classes = [AdminPermission] 
 