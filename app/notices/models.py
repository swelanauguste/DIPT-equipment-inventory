import uuid

from django.db import models
from django.utils.text import slugify
from users.models import User
from django.shortcuts import reverse


class Notice(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    message = models.TextField()
    priority = models.IntegerField(default=1)
    post = models.FileField(upload_to="announcements/", null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    draft = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    class Meta:
        ordering = ["-priority", "-created_at"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.uid)
        super(Notice, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("notice-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
