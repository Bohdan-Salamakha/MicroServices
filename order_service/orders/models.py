from django.db import models


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILURE = 'FAILURE', 'Failure'

    user_id = models.IntegerField()
    status = models.CharField(
        max_length=7,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk} by user with id {self.user_id}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of product ID {self.product_id}"
