"""Template context shared across every page (branding, navigation, footer)."""

from datetime import date


def site_context(request):
    # Imported lazily so this module stays importable before migrations run.
    from blog.models import Category

    return {
        "SITE_NAME": "Mots sur Maux",
        "SITE_TAGLINE": "Mettre des mots sur ses maux, à travers l'écriture.",
        "SITE_DESCRIPTION": (
            "Un projet artistique, thérapeutique, éducatif et social qui vise à "
            "favoriser le mieux-être psychologique et l'expression de soi à "
            "travers l'écriture."
        ),
        "NAV_CATEGORIES": Category.objects.all()[:6],
        "CURRENT_YEAR": date.today().year,
        # Affiché dans le pied de page de chaque page.
        "DISCLAIMER": (
            "Mots sur Maux s'inscrit dans une approche de prévention, "
            "d'humanisation et d'éducation émotionnelle, sans prétendre "
            "remplacer les services de santé mentale professionnels."
        ),
        # Ressource de crise (Canada).
        "CRISIS_NOTE": (
            "En cas de détresse, composez le 9-8-8 (ligne d'aide en cas de "
            "crise de suicide, Canada), disponible en tout temps."
        ),
    }
