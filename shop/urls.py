from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('success/', views.payment_success, name='payment-success'),
]