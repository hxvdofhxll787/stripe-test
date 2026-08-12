from django.test import TestCase
from django.urls import reverse

from decimal import Decimal
from unittest.mock import patch

from .models import Item, Order, OrderItem, Discount, Tax


class ItemViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Test Item',
            description='Test description',
            price=Decimal('100.24'),
            currency='usd',
        )

    def test_item_page(self):
        response = self.client.get(reverse('item-detail',args=[self.item.id]))

        self.assertContains(response, self.item.name)
        self.assertContains(response, self.item.description)
        self.assertContains(response, '100.24')

        self.assertIn('item', response.context)

    def test_item_page_returns_200(self):
        response = self.client.get(reverse('item-detail',args=[self.item.id]))

        self.assertEqual(response.status_code, 200)

    def test_item_page_returns_404(self):
        response = self.client.get(reverse('item-detail', args=[99999]))

        self.assertEqual(response.status_code, 404)

class BuyItemViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Test Item',
            description='Test description',
            price=Decimal('100.24'),
        )

    @patch('shop.views.PaymentService.create_checkout_session')
    def test_buy_item_returns_session_id(self, mock_session):
        mock_session.return_value.id = 'cs_test_012'

        response = self.client.get(reverse('buy-item',args=[self.item.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'cs_test_012')

class OrderModelTest(TestCase):
    def setUp(self):
        self.item_1 = Item.objects.create(
            name='Item 1',
            description='Description 1',
            price=Decimal('10.25'),
        )

        self.item_2 = Item.objects.create(
            name='Item 2',
            description='Description 2',
            price=Decimal('5.50'),
        )

    def test_order_total_price(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            item=self.item_1,
            quantity=2,
        )

        OrderItem.objects.create(
            order=order,
            item=self.item_2,
            quantity=3,
        )

        self.assertEqual(
            order.total_price,
            Decimal('37.00'),
        )

class TaxDiscountTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Item',
            description='Description',
            price=Decimal('100.24'),
        )

        self.discount = Discount.objects.create(
            name='Discount',
            percent=Decimal('20.00'),
        )

        self.tax = Tax.objects.create(
            name='Tax',
            percent=Decimal('28.00'),
        )

    def test_order_discount_and_tax(self):
        order = Order.objects.create(
            discount=self.discount,
            tax=self.tax,
        )

        OrderItem.objects.create(
            order=order,
            item=self.item,
            quantity=1,
        )

        self.assertEqual(
            order.subtotal,
            Decimal('100.24'),
        )

        self.assertEqual(
            order.discount_amount,
            Decimal('20.048'),
        )

        self.assertEqual(
            order.tax_amount,
            Decimal('22.45376'),
        )

        self.assertEqual(
            order.total_price,
            Decimal('102.64576'),
        )

