import stripe
from django.conf import settings
from shop.models import Item, Order, Discount, Tax, Discount

class PaymentService:
    def get_secret_key(self, currency: str):
        keys = {
            'usd': settings.STRIPE_USD_SECRET_KEY,
            'eur': settings.STRIPE_EUR_SECRET_KEY,
        }

        return keys[currency]

    def create_checkout_session(self, item: Item):
        api_key = self.get_secret_key(item.currency)

        client = stripe.StripeClient(api_key)

        session = client.v1.checkout.sessions.create(
            params={
                'line_items': [{
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100)
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                'success_url': f"{settings.SITE_URL}/success",
            }
        )

        return session

    def create_order_checkout_session(self, order: Order):
        api_key = self.get_secret_key(order.currency)

        client = stripe.StripeClient(api_key)

        line_items = []

        if order.tax:
            tax = self.create_tax(order.tax, client)

            tax_rate = [tax.id]
        else:
            tax_rate = []

        for order_item in order.order_items.select_related('item'):
            line_items.append(
                {
                    'price_data': {
                        'currency': order.currency,
                        'product_data': {
                            'name': order_item.item.name,
                            'description': order_item.item.description,
                        },
                        'unit_amount': int(order_item.item.price * 100),
                    },
                    'quantity': order_item.quantity,
                    'tax_rates': tax_rate,
                },
            )

        data = {
            'line_items': line_items,
            'mode': 'payment',
            'success_url': f"{settings.SITE_URL}/success",
        }

        if order.discount:
            coupon = self.create_coupon(order.discount, client)

            data['discounts'] = [{'coupon': coupon.id}]

        return client.v1.checkout.sessions.create(
            params={
                **data,
            }
        )

    def create_coupon(self, discount: Discount, client):
        coupon = client.v1.coupons.create({
            'duration': 'once',
            'name': discount.name,
            'percent_off': discount.percent,
        })

        return coupon

    def create_tax(self, tax: Tax, client):
        tax = client.v1.tax_rates.create({
            'display_name': tax.name,
            'percentage': tax.percent,
            'inclusive': False,
            'tax_type': 'sales_tax',
        })

        return tax