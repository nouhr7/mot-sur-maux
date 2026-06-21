from django.apps import AppConfig


class TeamConfig(AppConfig):
    """L'« Espace équipe » : une interface simple et conviviale pour publier.

    Cette application ne contient aucun modèle : elle offre une couche de
    rédaction agréable par-dessus les modèles existants (articles, ateliers,
    soumissions, demandes), réservée aux membres de l'équipe.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "team"
    verbose_name = "Espace équipe"
