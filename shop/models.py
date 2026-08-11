from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', related_name='orders')

    def __str__(self):
        return f'Order {self.id}'

    @property
    def total_price(self):
        return sum(order_item.total_price for order_item in self.order_items.all())

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
