from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Extra information attached to any user (member or staff).

    For now it holds an optional avatar, used as the photo in the team
    dashboard and on the member's personal space.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        "Photo de profil", upload_to="avatars/", blank=True, null=True
    )

    def __str__(self):
        return f"Profil de {self.user}"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.get_username()

    @property
    def initials(self):
        name = self.display_name
        parts = name.split()
        return "".join(p[0] for p in parts[:2]).upper() or name[:1].upper()


class JournalEntry(models.Model):
    """A private writing entry kept by a member over time.

    « Mots sur Maux » est un projet d'écriture : le journal permet de poser des
    mots pour soi, à son rythme. Privé par défaut.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journal_entries",
    )
    title = models.CharField("Titre", max_length=160, blank=True)
    content = models.TextField("Votre texte")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entrée de journal"
        verbose_name_plural = "Entrées de journal"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or f"Entrée du {self.created_at:%Y-%m-%d}"

    @property
    def display_title(self):
        return self.title or f"Entrée du {self.created_at:%-d %B %Y}"


class Bookmark(models.Model):
    """An article a member saved to read (again) later."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    article = models.ForeignKey(
        "blog.Article", on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article"], name="unique_bookmark"
            )
        ]


class ArticleRead(models.Model):
    """Tracks that a member has read an article (reading progress/history)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reads",
    )
    article = models.ForeignKey(
        "blog.Article", on_delete=models.CASCADE, related_name="reads"
    )
    read_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lecture"
        verbose_name_plural = "Lectures"
        ordering = ["-read_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article"], name="unique_read"
            )
        ]
