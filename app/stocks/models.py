import random
import string

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from users.models import User


def generate_short_id():
    length = 8  # You can adjust the length as needed
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length)).upper()


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(
        max_length=8, unique=True, editable=False, default=generate_short_id, null=True
    )  # Stock Keeping Unit
    slug = models.SlugField(unique=True, max_length=8, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(self.sku)
        super(Item, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("stock-detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE)
    quantity = models.PositiveIntegerField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.transaction_type == "IN":
            self.item.stock_quantity += self.quantity
        elif (
            self.transaction_type == "OUT" and self.item.stock_quantity >= self.quantity
        ):
            self.item.stock_quantity -= self.quantity
        self.item.save()
        
    def get_absolute_url(self):
        return reverse("trans-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.name} ({self.quantity})"
