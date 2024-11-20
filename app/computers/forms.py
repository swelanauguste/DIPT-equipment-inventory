from django import forms

from . import models


class ComputerForm(forms.ModelForm):
    class Meta:
        model = models.Computer
        fields = [
            "from_project",
            "serial_number",
            "warranty_info",
            "serial_number",
            "computer_name",
            "model",
            "status",
            "os",
            "location",
            "department",
            "user",
            "date_received",
            "date_installed",
            "image",
            "notes",
        ]


class ComputerModelForm(forms.ModelForm):
    class Meta:
        model = models.ComputerModel
        fields = "__all__"
        exclude = ["slug", "created_by", "updated_by"]
