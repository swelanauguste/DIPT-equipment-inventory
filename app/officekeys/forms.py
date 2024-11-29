from django import forms
from . import models
class MicrosoftOfficeForm(forms.ModelForm):
    class Meta:
        model = models.MicrosoftOffice
        fields = ["version", "product_key"]


class MicrosoftOfficeAssignmentForm(forms.ModelForm):
    class Meta:
        model = models.MicrosoftOfficeAssignment
        fields = ["computers", "date_assigned", "notes"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['computers'].queryset = models.Computer.objects.filter(
            office_key_computers__isnull=True
        )
