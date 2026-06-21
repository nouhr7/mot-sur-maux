from django.conf import settings
from django.db import models


class Submission(models.Model):
    """An anonymous submission shared through the online platform.

    « La plateforme accepte également des soumissions anonymes, permettant aux
    personnes de partager une situation, une question ou un malaise. »
    """

    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        IN_REVIEW = "in_review", "En traitement"
        PUBLISHED = "published", "A inspiré un article"
        ARCHIVED = "archived", "Archivée"

    topic = models.CharField(
        "Sujet / thème",
        max_length=160,
        blank=True,
        help_text="Facultatif — par ex. « anxiété », « rupture », « solitude ».",
    )
    feeling = models.CharField(
        "Comment te sens-tu en ce moment ?", max_length=160, blank=True
    )
    message = models.TextField(
        "Ce que tu souhaites partager",
        help_text="Une situation, une question ou un malaise. Tu restes anonyme.",
    )
    # Facultatif : une personne peut souhaiter être recontactée. Vide = anonyme.
    contact_email = models.EmailField("Courriel (facultatif)", blank=True)

    # Facultatif : si la personne était connectée, on relie la soumission à son
    # compte pour qu'elle la retrouve dans son historique. La modération reste
    # anonyme (ce lien n'est pas affiché dans l'espace équipe).
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Membre (historique)",
        on_delete=models.SET_NULL,
        related_name="submissions",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.NEW
    )
    moderator_notes = models.TextField("Notes de modération", blank=True)
    created_at = models.DateTimeField("Reçue le", auto_now_add=True)

    class Meta:
        verbose_name = "Soumission anonyme"
        verbose_name_plural = "Soumissions anonymes"
        ordering = ["-created_at"]

    def __str__(self):
        label = self.topic or "Soumission"
        return f"{label} — {self.created_at:%Y-%m-%d}"
