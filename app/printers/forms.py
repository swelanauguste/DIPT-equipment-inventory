from django import forms

from . import models


class PrinterForm(forms.ModelForm):
    class Meta:
        model = models.Printer
        fields = "__all__"
        exclude = ["created_by", "updated_by", "slug"]


class PrinterModelForm(forms.ModelForm):
    class Meta:
        model = models.PrinterModel
        fields = "__all__"
        exclude = ["created_by", "updated_by", "slug"]
