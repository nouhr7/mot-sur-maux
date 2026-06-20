from django.db import models


class ContactMessage(models.Model):
    """A message sent through the public contact form."""

    name = models.CharField("Nom", max_length=120)
    email = models.EmailField("Courriel")
    subject = models.CharField("Sujet", max_length=160, blank=True)
    message = models.TextField("Message")
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)
    is_handled = models.BooleanField("Traité", default=False)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or 'Sans sujet'}"


class Founder(models.Model):
    """A founder / core team member presented on the project page."""

    name = models.CharField("Nom", max_length=120, blank=True)
    role = models.CharField("Rôle", max_length=120, blank=True)
    bio = models.TextField("Présentation", blank=True)
    photo = models.ImageField("Photo", upload_to="founders/", blank=True, null=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Affiché", default=True)

    class Meta:
        verbose_name = "Fondateur·rice / équipe"
        verbose_name_plural = "Fondateur·rices / équipe"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name or f"Fondateur·rice #{self.pk or '?'}"

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()


class Partner(models.Model):
    """A partner organisation (schools, camps, community orgs)."""

    name = models.CharField("Nom", max_length=160)
    url = models.URLField("Site web", blank=True)
    logo = models.ImageField("Logo", upload_to="partners/", blank=True, null=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Affiché", default=True)

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
