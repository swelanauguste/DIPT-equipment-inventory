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
    image = models.FileField(upload_to="printer_models/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PrinterModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("printer-model-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.maker} - {self.name}"


class Printer(models.Model):
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    printer_name = models.CharField(max_length=255, blank=True, null=True)
    model = models.ForeignKey(
        PrinterModel, on_delete=models.CASCADE, related_name="printers"
    )
    ip_addr = models.GenericIPAddressField("IP Address", blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printer_locations",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printer_departments",
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
        related_name="printer_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_updated_by",
    )

    class Meta:
        ordering = ["-ip_addr"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.serial_number:
                self.slug = slugify(self.serial_number)
            elif self.printer_name:
                self.slug = slugify(self.printer_name)
            else:
                self.slug = slugify(get_random_string(length=8))
        super(Printer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("printer-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.model.maker} - {self.model.name}"



class PrinterComment(models.Model):
    printer = models.ForeignKey(
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
        related_name="printer_comment_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_comment_updated_by",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.printer.printer_name} - comment {self.pk}"
