from django import forms

from . import models


class ComputerForm(forms.ModelForm):
    class Meta:
        model = models.Computer
        fields = "__all__"
        exclude = ["slug", "created_by", "updated_by"]


class ComputerModelForm(forms.ModelForm):
    class Meta:
        model = models.ComputerModel
        fields = "__all__"
        exclude = ["slug", "created_by", "updated_by"]


class MonitorForm(forms.ModelForm):
    class Meta:
        model = models.Monitor
        fields = "__all__"
        exclude = ["slug", "created_by", "updated_by"]


class MonitorModelForm(forms.ModelForm):
    class Meta:
        model = models.MonitorModel
        fields = "__all__"
        exclude = ["slug", "created_by", "updated_by"]

