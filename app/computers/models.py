from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from users.models import Department, Location, User


class Maker(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Maker, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("maker-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name.upper()


class OperatingSystem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(OperatingSystem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("maker-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name.upper()


class Status(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Statuses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Status, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("maker-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name.upper()


class MonitorModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    maker = models.ForeignKey(
        Maker, on_delete=models.PROTECT, related_name="monitor_models"
    )
    image = models.FileField(upload_to="monitor_models/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{get_random_string(length=2)}")
        super(MonitorModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("monitor-model-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.maker.name.upper()} - {self.name.upper()}"


class Monitor(models.Model):
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    model = models.ForeignKey(
        MonitorModel, on_delete=models.PROTECT, related_name="monitors"
    )
    date_received = models.DateField(blank=True, null=True, default=timezone.now)
    date_installed = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="monitor_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="monitor_updated_by",
    )

    class Meta:
        ordering = ["model__name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.serial_number}-{get_random_string(length=2)}")
        super(Monitor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("monitor-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.model.name.upper()} - {self.serial_number.upper()}"


class ComputerModel(models.Model):
    computer_type_list = [
        ("desktop", "Desktop"),
        ("laptop", "Laptop"),
        ("tablet", "Tablet"),
        ("server", "Server"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    computer_type = models.CharField(
        max_length=10, choices=computer_type_list, default="desktop"
    )
    maker = models.ForeignKey(
        Maker, on_delete=models.PROTECT, related_name="computer_models"
    )
    processor = models.CharField(
        max_length=100, blank=True, null=True, help_text="In GHz(e.g.:i5 2.9 GHz)"
    )
    ram = models.CharField("RAM", max_length=5, blank=True, null=True, help_text="GB")
    hdd = models.CharField(max_length=5, verbose_name="HDD/Storage", help_text="GB/TB")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="computer_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="computer_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.processor, self.name}")
        super(ComputerModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("computer-model-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.maker} - {self.name.upper()} - {self.processor}"


class Computer(models.Model):
    from_project = models.BooleanField(default=False)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    warranty_info = models.CharField(
        "Warranty", max_length=100, default="N/A", blank=True, null=True
    )
    computer_name = models.CharField(
        max_length=100, blank=True, null=True, default="MCWT"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="computer_status",
        null=True,
        blank=True,
    )
    model = models.ForeignKey(
        ComputerModel,
        on_delete=models.PROTECT,
        related_name="computers",
        null=True,
        blank=True,
    )
    monitor = models.ManyToManyField(Monitor, related_name="monitors", blank=True)
    os = models.ForeignKey(
        OperatingSystem,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="computer_operating_systems",
        verbose_name="operating system",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="computer_locations",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="computer_departments",
    )
    user = models.ManyToManyField(User, related_name="computer_users", blank=True)
    date_received = models.DateField(blank=True, null=True, default=timezone.now)
    date_installed = models.DateField(blank=True, null=True)
    image = models.FileField(upload_to="system_audit/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="computer_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="computer_updated_by",
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.serial_number:
                self.slug = slugify(self.serial_number)
            elif self.computer_name:
                self.slug = slugify(self.computer_name)
            else:
                self.slug = slugify(get_random_string(length=8))
        super(Computer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("computer-detail", kwargs={"slug": self.slug})

    def get_last_computer_name(self):
        last_computer_name = Computer.objects.last()
        if last_computer_name:
            return last_computer_name.computer_name
        return "MCWT0000"

    def __str__(self):
        if self.serial_number:
            return self.serial_number.upper()
        return self.computer_name.upper()


class MicrosoftOfficeVersion(models.Model):
    name = models.CharField(max_length=20)
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
    product_key = models.CharField(max_length=30, unique=True)
    computer = models.ForeignKey(
        Computer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="serial number",
        related_name="office_installations",
    )
    date_installed = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    is_installed = models.BooleanField(default=False)
    has_failed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ms_office_created_by",
    )
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


class MicrosoftOfficeInstalled(models.Model):
    computer = models.ForeignKey(
        Computer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="office_installed",
    )
    microsoft_office = models.ForeignKey(
        MicrosoftOffice,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="installed_office",
    )
    date_installed = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    has_failed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_installed_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_installed_updated_by",
    )
