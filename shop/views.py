from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.conf import settings

from .models import Item
from .services.payment_service import PaymentService

def buy_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    payment_service = PaymentService()
    session = payment_service.create_checkout_session(item)

    return JsonResponse({
        'id': session.id,
    })

def item_detail(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    return render (request, 'shop/item.html', {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })