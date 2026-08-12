from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=3, choices=[('usd', 'USD'), ('eur', 'EUR')], default='USD')

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=200, unique=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.percent}%'

class Tax(models.Model):
    name = models.CharField(max_length=200, unique=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.percent}%'

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    currency = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f'Order {self.id}'

    @property
    def subtotal(self):
        return sum(order_item.total_price for order_item in self.order_items.all())

    @property
    def discount_amount(self):
        if not self.discount: return 0

        return self.subtotal * (self.discount.percent/100)

    @property
    def tax_amount(self):
        if not self.tax: return 0

        return (self.subtotal - self.discount_amount) * (self.tax.percent / 100)

    @property
    def total_price(self):
        return self.subtotal - self.discount_amount + self.tax_amount

    def update_currency(self, *args, **kwargs):
        currencies = self.order_items.values_list("item__currency", flat=True).distinct()

        if len(currencies) != 1:
            raise ValueError(f"Нельзя совмещать разные валюты!")

        self.currency = currencies[0]

        self.save(update_fields=['currency'])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'item'], name='unique_order_item')
        ]

    @property
    def total_price(self):
        return self.quantity * self.item.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.order.update_currency()

    def __str__(self):
        return f'{self.item.name} {self.quantity}'