# Standard lib imports
import datetime as dt

# Third-party imports
from crispy_forms.helper import FormHelper
from django import forms
from django.urls import reverse_lazy

# Project imports
from .models import Party, Gift

INVITATION_ERROR_MESSAGE = "You really should write an invitation."
DATE_PAST_ERROR_MESSAGE = "You chose a date in the past."

class PartyForm(forms.ModelForm):
    class Meta:
        model: type = Party
        fields: tuple = ("party_date", "party_time", "venue", "invitation")
        widgets: dict = {
            "party_date": forms.DateInput(attrs={
                "type": "date",
                "hx-get": reverse_lazy("partial_check_party_date"),
                "hx-trigger": "blur",
                "hx-swap": "outerHTML",
                "hx-target": "#div_id_party_date",
            }),
            "party_time": forms.TimeInput(attrs={
                "type": "time",
            }),
            "invitation": forms.Textarea(attrs={
                "class": "w-full",
                "hx-get": reverse_lazy("partial_check_invitation"),
                "hx-trigger": "blur",
                "hx-swap": "outerHTML",
                "hx-target": "#div_id_invitation",                
            }),
        }

    def clean_invitation(self):
        invitation: str = self.cleaned_data["invitation"]

        if len(invitation) < 10:
            raise forms.ValidationError(message=INVITATION_ERROR_MESSAGE)
        
        return invitation
    
    def clean_party_date(self):
        party_date: dt.date = self.cleaned_data["party_date"]

        if dt.date.today() > party_date:
            raise forms.ValidationError(message=DATE_PAST_ERROR_MESSAGE)
        
        return party_date
    
class GiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model: type = Gift
        fields: tuple = ("gift", "price", "link")