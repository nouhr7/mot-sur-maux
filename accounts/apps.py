from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Comptes des membres + profils (photo) partagés par tous les utilisateurs.

    Un compte n'est jamais obligatoire : le site reste entièrement utilisable
    de façon anonyme (lire les articles, soumettre un texte…). Le compte ajoute
    un espace personnel : journal privé, favoris, lectures et historique.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Comptes & espace personnel"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.models.signals import post_save

        from . import signals

        post_save.connect(signals.ensure_profile, sender=get_user_model())
