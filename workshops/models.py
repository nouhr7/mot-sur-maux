from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class HostType(models.TextChoices):
    SCHOOL = "school", "École"
    SUMMER_CAMP = "camp", "Camp d'été"
    COMMUNITY = "community", "Organisme communautaire"
    OTHER = "other", "Autre lieu partenaire"


class Workshop(models.Model):
    """An in-person writing workshop ("atelier en présentiel")."""

    title = models.CharField("Titre", max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    host_type = models.CharField(
        "Type de lieu", max_length=12, choices=HostType.choices, default=HostType.SCHOOL
    )
    location_name = models.CharField("Lieu", max_length=160, blank=True)
    city = models.CharField("Ville", max_length=120, blank=True)
    audience = models.CharField(
        "Public visé",
        max_length=160,
        blank=True,
        help_text="Ex. : jeunes de 12 à 17 ans, groupe communautaire…",
    )
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="workshops/", blank=True, null=True)

    starts_at = models.DateTimeField("Date et heure")
    ends_at = models.DateTimeField("Fin", blank=True, null=True)
    registration_url = models.URLField("Lien d'inscription", blank=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        verbose_name = "Atelier"
        verbose_name_plural = "Ateliers"
        ordering = ["starts_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:160] or "atelier"
            slug, counter = base, 2
            while Workshop.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("workshops:detail", args=[self.slug])

    @property
    def is_upcoming(self):
        return self.starts_at >= timezone.now()


class WorkshopRequest(models.Model):
    """An organisation requesting that a workshop be hosted at their location."""

    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        CONTACTED = "contacted", "Contact établi"
        SCHEDULED = "scheduled", "Planifié"
        DECLINED = "declined", "Refusé"

    organization_name = models.CharField("Nom de l'organisme", max_length=180)
    host_type = models.CharField(
        "Type de lieu", max_length=12, choices=HostType.choices, default=HostType.SCHOOL
    )
    contact_name = models.CharField("Personne-ressource", max_length=120)
    email = models.EmailField("Courriel")
    phone = models.CharField("Téléphone", max_length=40, blank=True)
    city = models.CharField("Ville", max_length=120, blank=True)
    audience = models.CharField(
        "Participants pressentis", max_length=200, blank=True
    )
    preferred_dates = models.CharField("Dates souhaitées", max_length=200, blank=True)
    message = models.TextField("Votre projet / vos besoins", blank=True)

    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande d'atelier"
        verbose_name_plural = "Demandes d'atelier"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.organization_name} ({self.get_status_display()})"
