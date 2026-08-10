import stripe

from django.conf import settings

from shop.models import Item

class PaymentService:
    def __init__(self):
        self.client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)

    def create_checkout_session(self, item: Item):
        session = self.client.v1.checkout.sessions.create(
            params={
                'line_items': [{
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100)
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                'success_url': f"{settings.SITE_URL}/success"
            }
        )

        return session