from django.urls import path

from . import views

urlpatterns = [
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
]