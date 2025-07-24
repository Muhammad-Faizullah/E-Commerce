from django.urls import path
from .views import OrderView,OrderListView,PaymentView,TaskView,FeedbackView,FeedbackViewForAdmin

urlpatterns = [
    path('',OrderView.as_view({"post":"order_product"})),
    path('List/',OrderListView.as_view({"get":"order_list"})),
    path('Payment/',PaymentView.as_view({"post":"payment"})),
    path('reminder/',TaskView.as_view({"get":"reminder"})),
    path('feedback/',FeedbackView.as_view()),
    path('feedback/<int:pk>/',FeedbackViewForAdmin.as_view())
]