from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('order-list/', views.order_list, name='order-list'),
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
    path('buy-order/<int:order_id>/', views.buy_order, name='buy-order'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('success/', views.payment_success, name='payment-success'),
]