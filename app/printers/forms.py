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


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.PrinterComment
        fields = ["comment"]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }
