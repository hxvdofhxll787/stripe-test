from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Item
from .services.payment_service import PaymentService

def buy_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)

    payment_service = PaymentService()
    session = payment_service.create_checkout_session(item)

    return JsonResponse({
        'id': session.id,
    })