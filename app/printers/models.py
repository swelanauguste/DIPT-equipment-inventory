from computers.models import Maker, Status
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from users.models import Department, Location, User


class PrinterModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    image = models.FileField(upload_to="device_models/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PrinterModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("device-model-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.maker} - {self.name}"


class Printer(models.Model):
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    model = models.ForeignKey(
        PrinterModel, on_delete=models.CASCADE, related_name="devices"
    )
    ip_addr = models.GenericIPAddressField("IP Address", blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="device_locations",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="device_departments",
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_received = models.DateField(blank=True, null=True, default=timezone.now)
    date_installed = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_updated_by",
    )

    class Meta:
        ordering = ["-ip_addr"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.serial_number:
                self.slug = slugify(self.serial_number)
            elif self.name:
                self.slug = slugify(self.name)
            else:
                self.slug = slugify(get_random_string(length=8))
        super(Printer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("device-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.model.maker} - {self.model.name}"



class PrinterComment(models.Model):
    device = models.ForeignKey(
        Printer, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_comment_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="device_comment_updated_by",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.device.device_name} - comment {self.pk}"
