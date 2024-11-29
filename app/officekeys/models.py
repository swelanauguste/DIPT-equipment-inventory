from computers.models import Computer
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from users.models import User


class MicrosoftOfficeVersion(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="version_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="version_updated_by",
    )

    def __str__(self):
        return f"Microsoft Office {self.name}"


class MicrosoftOffice(models.Model):
    version = models.ForeignKey(
        MicrosoftOfficeVersion,
        on_delete=models.CASCADE,
        related_name="versions",
        default=1,
    )
    product_key = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ms_office_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ms_office_updated_by",
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("microsoft-office-detail", kwargs={"pk": self.pk})

    def remove_hyphens(self):
        return self.product_key.replace("-", "")

    def __str__(self):
        return f"{self.version} - XXXXX-XXXXX-XXXXX-{self.product_key[-11:]}"


class MicrosoftOfficeAssignment(models.Model):
    microsoft_office = models.ForeignKey(
        MicrosoftOffice, on_delete=models.CASCADE, related_name="assignments"
    )
    computers = models.ManyToManyField(Computer, related_name="office_key_computers")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_key_created_by",
    )
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_key_updated_by",
    )
    date_assigned = models.DateField(default=timezone.now)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_key_assigned_by",
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("microsoft-office-assignment-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.microsoft_office}"
