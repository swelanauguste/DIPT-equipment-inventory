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
        
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if ComputerModel.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug already exists. Please choose a unique one.")
        return slug


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


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.ComputerComment
        fields = ["comment"]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }
