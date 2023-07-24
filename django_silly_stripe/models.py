import uuid

import stripe

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Customer(models.Model):
    id = models.CharField(
        max_length=100, unique=True,
        primary_key=True
        )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        default=None,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        )
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"<Customer: {self.user.email}>"


class Product(models.Model):
    id = models.CharField(
        max_length=100, unique=True,
        primary_key=True
        )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        )
    description = models.TextField(
        blank=True,
        null=True,
        )
    metadata = models.JSONField(
        blank=True,
        null=True,
        )
    images = models.JSONField(
        blank=True,
        null=True,
        )
    active = models.BooleanField(
        default=True,
        )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"<Product: {self.name}>"


class Price(models.Model):
    id = models.CharField(
        max_length=100, unique=True,
        primary_key=True
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prices',
        default=None,
    )
    unit_amount = models.IntegerField(
        blank=True,
        null=True,
        )
    currency = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        )
    recurring_interval = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        )
    recurring_interval_count = models.IntegerField(
        blank=True,
        null=True,
        )
    active = models.BooleanField(
        default=True,
        )
    metadata = models.JSONField(
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"

    def __str__(self):
        return f"<Price: {self.product.name}>"
