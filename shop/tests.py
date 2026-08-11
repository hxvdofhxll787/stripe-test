from django.test import TestCase
from django.urls import reverse

from decimal import Decimal
from unittest.mock import patch

from .models import Item

class ItemViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Test Item',
            description='Test description',
            price=Decimal('100.24'),
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