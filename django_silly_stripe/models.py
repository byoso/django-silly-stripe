import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Customer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    stripe_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stripe_customer',
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"<Customer: {self.user.email}>"
