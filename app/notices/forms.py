from django import forms

from .models import Notice


class NoticeCreateForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["expiration_date", "priority", "post", "title", "message"]
        widgets = {
            "title": forms.Textarea(attrs={"class": "notice-title"}),
            "message": forms.Textarea(attrs={"class": "notice-message"}),
            "expiration_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
