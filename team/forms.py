from django import forms

from blog.models import Article
from submissions.models import Submission
from workshops.models import Workshop

from .sanitize import clean_html, strip_tags

# Reusable widget styling hooks. The actual look comes from styles.css /
# team.css, which already style .form-field inputs nicely.
_DATETIME_FORMATS = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]


class ArticleForm(forms.ModelForm):
    """Friendly create/edit form for an article.

    Publication (draft vs. published) is handled by the view via named submit
    buttons, so it is deliberately *not* a field here. ``content`` holds the
    HTML produced by the visual editor and is sanitised on the way in.
    """

    class Meta:
        model = Article
        fields = [
            "title", "category", "author", "excerpt",
            "content", "content_warning",
            "cover_image", "cover_credit", "is_featured",
        ]
        labels = {
            "title": "Titre de l'article",
            "category": "Thématique",
            "author": "Signé par",
            "excerpt": "Chapeau (résumé court)",
            "content": "Contenu",
            "content_warning": "Avertissement de contenu",
            "cover_image": "Image de couverture",
            "cover_credit": "Crédit de l'image",
            "is_featured": "Mettre à la une",
        }
        help_texts = {
            "excerpt": "Une ou deux phrases qui donnent envie de lire. "
                       "Affiché dans les listes et en introduction.",
            "content_warning": "Laissez vide si l'article n'aborde rien de sensible. "
                               "Sinon, nommez le sujet (ex. : « suicide », « automutilation »).",
            "cover_image": "Facultatif. Une belle image en haut de l'article.",
            "is_featured": "L'article apparaîtra en vedette sur la page Articles.",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Le titre de votre article"}
            ),
            "excerpt": forms.Textarea(
                attrs={"rows": 2,
                       "placeholder": "Ex. : Quand l'anxiété prend toute la place, "
                                      "écrire devient une respiration."}
            ),
            # Hidden: the visible editor (Quill) writes its HTML in here.
            "content": forms.Textarea(attrs={"id": "id_content", "hidden": True}),
            "content_warning": forms.TextInput(
                attrs={"placeholder": "Ex. : suicide, automutilation"}
            ),
            "cover_credit": forms.TextInput(
                attrs={"placeholder": "Ex. : Photo de Jean Dupont"}
            ),
        }

    def clean_content(self):
        html = clean_html(self.cleaned_data.get("content", ""))
        if not strip_tags(html).strip():
            raise forms.ValidationError(
                "L'article a besoin d'un contenu avant d'être enregistré."
            )
        return html


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = [
            "title", "host_type", "location_name", "city", "audience",
            "description", "image", "starts_at", "ends_at",
            "registration_url", "is_published",
        ]
        labels = {
            "title": "Titre de l'atelier",
            "host_type": "Type de lieu",
            "location_name": "Nom du lieu",
            "city": "Ville",
            "audience": "Public visé",
            "description": "Description",
            "image": "Image",
            "starts_at": "Date et heure de début",
            "ends_at": "Fin (facultatif)",
            "registration_url": "Lien d'inscription (facultatif)",
            "is_published": "Visible sur le site",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Ex. : Atelier d'écriture — mettre des mots sur ses maux"}
            ),
            "location_name": forms.TextInput(
                attrs={"placeholder": "Ex. : École secondaire des Sources"}
            ),
            "audience": forms.TextInput(
                attrs={"placeholder": "Ex. : jeunes de 12 à 17 ans"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 5,
                       "placeholder": "Décrivez l'atelier : déroulement, intention, ambiance…"}
            ),
            "starts_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "ends_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "registration_url": forms.URLInput(
                attrs={"placeholder": "https://…"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["starts_at"].input_formats = _DATETIME_FORMATS
        self.fields["ends_at"].input_formats = _DATETIME_FORMATS


class SubmissionStatusForm(forms.ModelForm):
    """Lets the team triage an anonymous submission."""

    class Meta:
        model = Submission
        fields = ["status", "moderator_notes"]
        labels = {
            "status": "Où en est cette soumission ?",
            "moderator_notes": "Notes internes (privées)",
        }
        widgets = {
            "moderator_notes": forms.Textarea(
                attrs={"rows": 4,
                       "placeholder": "Notes pour l'équipe : suivi, idée d'article, etc."}
            ),
        }
