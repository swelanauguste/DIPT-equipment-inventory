from django import forms
from users.models import User

from .models import Ticket


class TicketUserForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role__in=["technician", "manager"]),
        widget=forms.Select,
        required=False,
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = [
            "ticket_id",
            "slug",
            "ticket_status",
            "ticket_category",
            "created_by",
            "updated_by",
        ]


class TicketTechCreateForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role__in=["technician", "manager"]),
        widget=forms.Select,
        required=False,
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ["ticket_id", "slug", "created_by", "updated_by"]


class TicketTechUpdateForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role__in=["technician", "manager"]),
        widget=forms.Select,
        required=False,
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = [
            "user",
            "ticket_id",
            "slug",
            "summary",
            "description",
            "created_by",
            "updated_by",
        ]
