from django import forms

from .models import Submission


class SubmissionForm(forms.ModelForm):
    # Honeypot anti-pourriel : invisible pour les humains, rempli par les robots.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Submission
        fields = ["topic", "feeling", "message", "contact_email"]
        widgets = {
            "topic": forms.TextInput(
                attrs={"placeholder": "Ex. : anxiété, solitude, rupture…"}
            ),
            "feeling": forms.TextInput(
                attrs={"placeholder": "Quelques mots, si tu le souhaites"}
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "Prends le temps d'écrire ce que tu ressens. "
                    "Il n'y a pas de bonne ou de mauvaise façon de le dire.",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={"placeholder": "Seulement si tu souhaites une réponse"}
            ),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Soumission invalide.")
        return ""
