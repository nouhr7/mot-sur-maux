"""Template context shared across every page (branding, navigation, footer)."""

from datetime import date


def site_context(request):
    # Imported lazily so this module stays importable before migrations run.
    from blog.models import Category

    return {
        "SITE_NAME": "Mots sur Maux",
        "SITE_TAGLINE": "Mettre des mots sur ses maux, à travers l'écriture.",
        "SITE_DESCRIPTION": (
            "Un projet d'éducation à l'expression des émotions : guider chacun, "
            "et les jeunes en particulier, à mettre des mots sur les maux qui les "
            "traversent — à travers l'écriture."
        ),
        "NAV_CATEGORIES": Category.objects.all()[:6],
        "CURRENT_YEAR": date.today().year,
        # Coordonnées pour la prise de rendez-vous d'ateliers (à personnaliser).
        "CONTACT_EMAIL": "bonjour@motssurmaux.ca",
        "CONTACT_PHONE": "",
        # Affiché dans le pied de page de chaque page.
        "DISCLAIMER": (
            "Mots sur Maux est un projet d'éducation et de prévention. Il ne "
            "remplace pas un suivi ni les services de santé mentale professionnels."
        ),
        # Ressource de crise (Canada).
        "CRISIS_NOTE": (
            "En cas de détresse ou de pensées suicidaires, composez ou textez le "
            "9-8-8 (ligne d'aide en cas de crise de suicide, Canada), 24 h/24."
        ),
    }
