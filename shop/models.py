from django.db import models
from stripe import Discount
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=200, unique=True)
    percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.percent}%'

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return f'Order {self.id}'

    @property
    def total_price(self):
        return sum(order_item.total_price for order_item in self.order_items.all())

    @property
    def total_price_with_discount(self):
        if not self.discount: return self.total_price

        return self.total_price * (1 - self.discount.percent/100)

    @property
    def discount_amount(self):
        if not self.discount: return 0

        return self.total_price - self.total_price_with_discount

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

    def __str__(self):
        return f'{self.item.name} {self.quantity}'