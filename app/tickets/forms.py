from django import forms
from users.models import User

from .models import Comment, Ticket


class TicketUserForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["summary", "description", "file"]


class TicketTechCreateForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = [
            "ticket_id",
            "slug",
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted_at",
            "is_deleted",
        ]

    def __init__(self, *args, **kwargs):
        # Extract additional parameters if passed
        roles = kwargs.pop("roles", ["technician", "manager"])
        super().__init__(*args, **kwargs)

        # Dynamically filter the queryset for the 'assigned_to' field
        self.fields["assigned_to"].queryset = User.objects.filter(role__in=roles)


class TicketTechUpdateForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["ticket_status", "ticket_category", "assigned_to"]

    def __init__(self, *args, **kwargs):
        # Extract additional parameters if passed
        roles = kwargs.pop("roles", ["technician", "manager"])
        super().__init__(*args, **kwargs)

        # Dynamically filter the queryset for the 'assigned_to' field
        self.fields["assigned_to"].queryset = User.objects.filter(role__in=roles)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comments"]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }
