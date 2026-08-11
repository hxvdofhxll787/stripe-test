from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET

from .models import Item, Order
from .services.payment_service import PaymentService

@require_GET
def buy_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    payment_service = PaymentService()
    session = payment_service.create_checkout_session(item)

    return JsonResponse({
        'id': session.id,
    })

@require_GET
def buy_order(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    payment_service = PaymentService()
    session = payment_service.create_order_checkout_session(order)

    return JsonResponse({
        'id': session.id,
    })

def item_detail(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    return render(request, 'shop/item.html', {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

def order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    items = order.order_items.all()

    return render(request, 'shop/order.html', {
        'order': order,
        'items': items,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

def payment_success(request):
    return render(request, 'shop/payment_success.html')

def item_list(request):
    items = Item.objects.all()

    return render(request, 'shop/item_list.html', { 'items': items })

def order_list(request):
    orders = Order.objects.all()

    return render(request, 'shop/order_list.html', { 'orders': orders })