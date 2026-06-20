from django.db import models


class ResourceCategory(models.Model):
    """A type of situation (suicidal thoughts, grief, anxiety, ...)."""

    name = models.CharField("Situation", max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.CharField("Description courte", max_length=240, blank=True)
    # Une situation peut être mise en avant (encadré d'urgence).
    is_urgent = models.BooleanField("Situation d'urgence", default=False)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Catégorie de ressource"
        verbose_name_plural = "Catégories de ressources"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Resource(models.Model):
    """A concrete help resource: a helpline, a centre, a website."""

    category = models.ForeignKey(
        ResourceCategory,
        verbose_name="Situation",
        related_name="resources",
        on_delete=models.CASCADE,
    )
    name = models.CharField("Nom", max_length=160)
    description = models.TextField("Description", blank=True)
    phone = models.CharField("Téléphone", max_length=60, blank=True)
    text_number = models.CharField("Texto", max_length=60, blank=True)
    url = models.URLField("Site web", blank=True)
    availability = models.CharField(
        "Disponibilité", max_length=120, blank=True, help_text="Ex. : 24 h/24, 7 j/7"
    )
    region = models.CharField(
        "Région", max_length=120, blank=True, help_text="Ex. : Canada, Québec…"
    )
    order = models.PositiveIntegerField("Ordre", default=0)
    is_active = models.BooleanField("Affiché", default=True)

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
