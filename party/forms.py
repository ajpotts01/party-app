# Third-party imports
from django import forms

# Project imports
from .models import Party

class PartyForm(forms.ModelForm):
    class Meta:
        model: type = Party
        fields: tuple = ("party_date", "party_time", "venue", "invitation")
        widgets: dict = {
            "party_date": forms.DateInput(attrs={
                "type": "date",
            }),
            "party_time": forms.TimeInput(attrs={
                "type": "time",
            }),
            "invitation": forms.Textarea(attrs={
                "class": "w-full",
            }),
        }