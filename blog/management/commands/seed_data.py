"""Populate the database with sample content for Mots sur Maux.

Usage:
    python manage.py seed_data
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Article, Category
from workshops.models import HostType, Workshop

CATEGORIES = [
    ("Anxiété", "#1c5c49", "Comprendre et apprivoiser l'anxiété au quotidien."),
    ("Dépendance affective", "#2e7d5b", "Quand le lien à l'autre fait vaciller le lien à soi."),
    ("Perte de repères", "#3d6b53", "Se retrouver lorsque tout semble flou."),
    ("Estime de soi", "#4a7c59", "Réapprendre à se regarder avec douceur."),
    ("Solitude", "#2b5d4a", "Mettre des mots sur le sentiment d'être seul."),
]

ARTICLES = [
    {
        "title": "Quand l'anxiété parle plus fort que nous",
        "category": "Anxiété",
        "featured": True,
        "excerpt": (
            "L'anxiété n'est pas un ennemi à abattre, mais un signal à écouter. "
            "Et si écrire ce qu'elle nous murmure aidait à en desserrer l'étreinte ?"
        ),
        "content": (
            "Il y a des matins où le cœur s'emballe avant même que la journée commence. "
            "L'anxiété s'installe, diffuse, sans qu'on sache toujours nommer ce qui l'a "
            "déclenchée. Elle se loge dans le souffle, dans les épaules, dans cette boule "
            "au ventre qui ne dit pas son nom.\n\n"
            "Pourtant, l'anxiété n'arrive jamais sans raison. Elle est souvent la trace "
            "d'un besoin non entendu : besoin de sécurité, de repos, de reconnaissance. "
            "Lorsqu'on prend le temps de l'écrire, de poser sur le papier ce qu'elle "
            "cherche à protéger, elle perd un peu de son pouvoir.\n\n"
            "Essayez ceci : la prochaine fois qu'elle monte, écrivez trois phrases qui "
            "commencent par « J'ai peur que… ». Sans vous juger. Mettre des mots sur la "
            "peur, c'est déjà commencer à la rendre habitable.\n\n"
            "L'écriture ne fait pas disparaître l'anxiété, mais elle transforme le silence "
            "en dialogue. Et un dialogue, même avec soi-même, est toujours moins lourd "
            "qu'un cri retenu."
        ),
    },
    {
        "title": "Aimer sans se perdre : comprendre la dépendance affective",
        "category": "Dépendance affective",
        "excerpt": (
            "Avoir besoin des autres est humain. Mais quand le lien devient la seule "
            "source de notre valeur, il est temps de revenir vers soi."
        ),
        "content": (
            "La dépendance affective n'est pas un défaut de caractère. C'est souvent une "
            "histoire ancienne, celle d'un amour qu'il fallait mériter, d'une présence "
            "jamais tout à fait certaine.\n\n"
            "On la reconnaît à cette peur de l'abandon qui pousse à tout donner, quitte à "
            "s'oublier. À ce vide qui surgit dès que l'autre s'éloigne.\n\n"
            "Écrire peut devenir un premier pas vers l'autonomie émotionnelle. Tenir un "
            "carnet où l'on note ce que l'on ressent — pas ce que l'autre ressent — aide "
            "à reconstruire un centre intérieur stable.\n\n"
            "Se choisir n'est pas renoncer à aimer. C'est apprendre à aimer depuis un lieu "
            "plus solide en soi."
        ),
    },
    {
        "title": "Perdre ses repères, et apprendre à se réorienter",
        "category": "Perte de repères",
        "excerpt": (
            "Un déménagement, une rupture, un deuil : parfois la carte intérieure se "
            "brouille. Comment retrouver un cap quand tout semble flou ?"
        ),
        "content": (
            "Il y a des périodes où l'on ne se reconnaît plus. Les certitudes d'hier "
            "n'ont plus de prise, et l'avenir reste illisible.\n\n"
            "Cette perte de repères, aussi déstabilisante soit-elle, est souvent le signe "
            "d'une transformation en cours. On ne se perd jamais tout à fait : on se "
            "cherche.\n\n"
            "Écrire ce que l'on ne sait plus — « je ne sais plus si… », « j'ai perdu… » — "
            "permet de cartographier le brouillard. Et dans ce brouillard mis en mots "
            "apparaissent parfois de nouveaux chemins.\n\n"
            "Donnez-vous la permission de ne pas tout comprendre maintenant. Les repères "
            "se reconstruisent un mot à la fois."
        ),
    },
    {
        "title": "La douceur, ce langage qu'on oublie de se parler",
        "category": "Estime de soi",
        "excerpt": (
            "Nous sommes souvent notre juge le plus sévère. Et si l'on apprenait à "
            "s'adresser à soi comme à un ami cher ?"
        ),
        "content": (
            "Observez la voix intérieure qui commente vos journées. Pour beaucoup, elle "
            "est dure, exigeante, prompte au reproche.\n\n"
            "Pourtant, cette voix n'est pas une vérité : c'est une habitude. Et les "
            "habitudes s'écrivent autrement.\n\n"
            "Un exercice simple : écrivez la lettre que vous adresseriez à un ami qui "
            "traverse exactement ce que vous vivez. Puis relisez-la en vous l'adressant à "
            "vous-même.\n\n"
            "L'estime de soi ne se décrète pas, elle se cultive — par de petits gestes de "
            "bienveillance répétés, jusqu'à ce qu'ils deviennent une langue maternelle."
        ),
    },
    {
        "title": "Se sentir seul, même entouré",
        "category": "Solitude",
        "excerpt": (
            "La solitude n'est pas toujours une question de présence. Parfois, c'est le "
            "sentiment de ne pas être vu, ni compris."
        ),
        "content": (
            "On peut être au milieu des autres et se sentir profondément seul. Cette "
            "solitude-là ne se soigne pas avec du bruit, mais avec du lien vrai.\n\n"
            "Mettre des mots sur ce sentiment, c'est déjà tendre une main — vers soi "
            "d'abord. Nommer « je me sens seul » brise un peu l'isolement, car cela "
            "rappelle que ce vécu est partagé par tant d'autres.\n\n"
            "La plateforme Mots sur Maux existe pour cela : pour que des mots, même "
            "anonymes, puissent rejoindre quelqu'un, quelque part, et lui dire qu'il "
            "n'est pas seul."
        ),
    },
]

WORKSHOPS = [
    {
        "title": "Atelier d'écriture émotionnelle — secondaire",
        "host_type": HostType.SCHOOL,
        "location_name": "École secondaire De la Rive",
        "city": "Gatineau",
        "audience": "Élèves de 13 à 16 ans",
        "days": 18,
        "description": (
            "Un atelier d'écriture guidée pour explorer ses émotions sans pression de "
            "performance. À travers des exercices simples et collectifs, les participants "
            "apprennent à mettre des mots sur ce qu'ils ressentent.\n"
            "Aucune expérience d'écriture requise. L'accent est mis sur le processus, "
            "pas sur le résultat."
        ),
    },
    {
        "title": "Mots et émotions — camp d'été",
        "host_type": HostType.SUMMER_CAMP,
        "location_name": "Camp Boisé",
        "city": "Wakefield",
        "audience": "Jeunes de 9 à 12 ans",
        "days": 32,
        "description": (
            "Une matinée créative où l'écriture rencontre le jeu. Les enfants découvrent "
            "que les mots peuvent devenir des amis pour dire la joie, la peur ou la "
            "colère.\nUne approche inclusive, qui privilégie l'oralité et "
            "l'accompagnement adapté."
        ),
    },
    {
        "title": "Cercle d'écriture — organisme communautaire",
        "host_type": HostType.COMMUNITY,
        "location_name": "Maison de quartier Saint-Cœur",
        "city": "Ottawa",
        "audience": "Adultes, groupe ouvert",
        "days": 45,
        "description": (
            "Un cercle d'écriture bienveillant pour adultes, autour de thèmes liés au "
            "vécu émotionnel. Un espace sécuritaire pour poser des mots, à son rythme, "
            "en toute confidentialité."
        ),
    },
]


class Command(BaseCommand):
    help = "Crée des catégories, articles et ateliers de démonstration."

    def handle(self, *args, **options):
        now = timezone.now()

        categories = {}
        for i, (name, color, desc) in enumerate(CATEGORIES):
            cat, _ = Category.objects.get_or_create(
                name=name, defaults={"color": color, "description": desc, "order": i}
            )
            categories[name] = cat
        self.stdout.write(self.style.SUCCESS(f"{len(categories)} catégories prêtes."))

        created = 0
        for offset, data in enumerate(ARTICLES):
            obj, was_created = Article.objects.get_or_create(
                title=data["title"],
                defaults={
                    "category": categories[data["category"]],
                    "excerpt": data["excerpt"],
                    "content": data["content"],
                    "is_published": True,
                    "is_featured": data.get("featured", False),
                    "published_at": now - timedelta(days=offset * 3),
                },
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} nouveaux articles créés."))

        w_created = 0
        for data in WORKSHOPS:
            _, was_created = Workshop.objects.get_or_create(
                title=data["title"],
                defaults={
                    "host_type": data["host_type"],
                    "location_name": data["location_name"],
                    "city": data["city"],
                    "audience": data["audience"],
                    "description": data["description"],
                    "starts_at": now + timedelta(days=data["days"]),
                    "is_published": True,
                },
            )
            w_created += was_created
        self.stdout.write(self.style.SUCCESS(f"{w_created} nouveaux ateliers créés."))
        self.stdout.write(self.style.SUCCESS("Données de démonstration prêtes."))
