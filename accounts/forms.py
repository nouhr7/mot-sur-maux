from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import JournalEntry, Profile

User = get_user_model()


class SignupForm(UserCreationForm):
    """Friendly account creation for visitors who want a personal space."""

    first_name = forms.CharField(
        label="Prénom", max_length=150, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Comment souhaitez-vous être appelé·e ?"}),
    )
    email = forms.EmailField(
        label="Courriel", required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Pour récupérer votre compte (facultatif)"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "username", "email"]
        labels = {"username": "Identifiant"}
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Un nom d'utilisateur"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.email = self.cleaned_data.get("email", "")
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Edit the avatar and the display name (first name)."""

    first_name = forms.CharField(
        label="Prénom affiché", max_length=150, required=False
    )

    class Meta:
        model = Profile
        fields = ["avatar"]
        labels = {"avatar": "Photo de profil"}
        help_texts = {"avatar": "JPG ou PNG. Carrée de préférence."}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None and not self.is_bound:
            self.fields["first_name"].initial = user.first_name

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if self.user is not None:
            self.user.first_name = self.cleaned_data.get("first_name", "")
            if commit:
                self.user.save(update_fields=["first_name"])
        return profile


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["title", "content"]
        labels = {"title": "Titre (facultatif)", "content": "Votre texte"}
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Un titre, si vous le souhaitez"}
            ),
            "content": forms.Textarea(
                attrs={"rows": 12,
                       "placeholder": "Écrivez librement. Personne d'autre que vous ne lira ces mots."}
            ),
        }
