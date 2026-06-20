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
