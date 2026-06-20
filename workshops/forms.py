from django import forms

from .models import WorkshopRequest


class WorkshopRequestForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    class Meta:
        model = WorkshopRequest
        fields = [
            "organization_name",
            "host_type",
            "contact_name",
            "email",
            "phone",
            "city",
            "audience",
            "preferred_dates",
            "message",
        ]
        widgets = {
            "audience": forms.TextInput(
                attrs={"placeholder": "Ex. : 25 jeunes de 10 à 14 ans"}
            ),
            "preferred_dates": forms.TextInput(
                attrs={"placeholder": "Ex. : semaine du 12 mai, avant-midi"}
            ),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Soumission invalide.")
        return ""
