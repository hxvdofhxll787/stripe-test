from django.urls import path

from . import views

urlpatterns = [
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
]