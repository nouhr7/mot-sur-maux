import math
import re

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """A theme of the online platform (anxiété, dépendance affective, ...)."""

    name = models.CharField("Nom", max_length=80, unique=True)
    slug = models.SlugField("Identifiant URL", max_length=90, unique=True, blank=True)
    description = models.CharField("Description courte", max_length=240, blank=True)
    # Couleur d'accent (hex) utilisée pour les étiquettes de catégorie.
    color = models.CharField("Couleur (hex)", max_length=7, default="#1c5c49")
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])

    @property
    def article_count(self):
        return self.articles(manager="published").count()


class Author(models.Model):
    """Someone who writes articles on the platform.

    « Je veux qu'on puisse cliquer sur le nom de l'auteur → ça dirige vers une
    page de l'auteur (biographie). »
    """

    name = models.CharField("Nom affiché", max_length=120)
    slug = models.SlugField("Identifiant URL", max_length=140, unique=True, blank=True)
    role = models.CharField(
        "Rôle / titre",
        max_length=120,
        blank=True,
        help_text="Ex. : Autrice invitée, Collectif, Bénévole…",
    )
    bio = models.TextField("Biographie", blank=True)
    photo = models.ImageField("Photo", upload_to="authors/", blank=True, null=True)
    email = models.EmailField("Courriel (facultatif)", blank=True)
    website = models.URLField("Site / réseau (facultatif)", blank=True)
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auteur·rice"
        verbose_name_plural = "Auteur·rices"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:120] or "auteur"
            slug, counter = base, 2
            while Author.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:author", args=[self.slug])

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()

    @property
    def article_count(self):
        return self.articles(manager="published").count()


class PublishedManager(models.Manager):
    """Only articles that are published and whose date has passed."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_published=True, published_at__lte=timezone.now())
        )


class Article(models.Model):
    """An article published on the online platform (le blog)."""

    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Identifiant URL", max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Catégorie",
        related_name="articles",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        Author,
        verbose_name="Auteur·rice",
        related_name="articles",
        on_delete=models.PROTECT,
    )
    excerpt = models.TextField(
        "Chapeau / résumé",
        max_length=320,
        help_text="Court résumé affiché dans les listes et l'aperçu.",
    )
    content = models.TextField(
        "Contenu",
        help_text="Séparez les paragraphes par une ligne vide.",
    )
    cover_image = models.ImageField(
        "Image de couverture", upload_to="articles/", blank=True, null=True
    )
    cover_credit = models.CharField("Crédit photo", max_length=160, blank=True)

    content_warning = models.CharField(
        "Avertissement de contenu",
        max_length=200,
        blank=True,
        help_text="Si l'article aborde un sujet sensible (suicide, automutilation, "
        "violence…), nommez-le ici. Un encadré bienveillant s'affichera avant le texte.",
    )

    is_published = models.BooleanField("Publié", default=False)
    is_featured = models.BooleanField("À la une", default=False)
    published_at = models.DateTimeField("Date de publication", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Un article peut naître d'une soumission anonyme reçue sur la plateforme.
    source_submission = models.ForeignKey(
        "submissions.Submission",
        verbose_name="Issu de la soumission",
        related_name="articles",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["-published_at"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "article"
            slug, counter = base, 2
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:article_detail", args=[self.slug])

    @property
    def paragraphs(self):
        """Split the raw content into clean paragraphs for templates."""
        return [p.strip() for p in re.split(r"\n\s*\n", self.content) if p.strip()]

    @property
    def body_html(self):
        """Render the article body for templates.

        Articles written in the team's visual editor are stored as
        (sanitised) HTML; older or admin-typed articles are plain text with
        blank-line-separated paragraphs. We detect which it is and return
        safe HTML either way.
        """
        from django.utils.html import escape
        from django.utils.safestring import mark_safe

        from team.sanitize import clean_html

        content = self.content or ""
        if re.search(
            r"</(p|h2|h3|h4|ul|ol|li|blockquote|strong|em|b|i|u|a)>",
            content,
            re.IGNORECASE,
        ):
            # HTML body. Sanitise on output too, so even content entered
            # directly in the admin (bypassing the editor form) is safe.
            return mark_safe(clean_html(content))
        paragraphs = "".join(f"<p>{escape(p)}</p>" for p in self.paragraphs)
        return mark_safe(paragraphs)

    @property
    def reading_minutes(self):
        text = re.sub(r"<[^>]+>", " ", self.content or "")
        words = len(re.findall(r"\w+", text))
        return max(1, math.ceil(words / 200))
