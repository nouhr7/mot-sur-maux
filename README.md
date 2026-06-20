# Mots sur Maux

> Mettre des mots sur ses maux, à travers l'écriture.

**Mots sur Maux** est un projet à la fois artistique, thérapeutique, éducatif et
social qui vise à favoriser le mieux-être psychologique et l'expression de soi à
travers l'écriture. Ce dépôt contient le site web du projet.

Le site est construit autour des **deux volets** du projet :

1. **Des ateliers en présentiel** — organisés dans des écoles, camps d'été et
   organismes communautaires, pour offrir des espaces sécuritaires d'expression.
2. **Une plateforme en ligne** — un blog d'articles sur le vécu émotionnel
   (anxiété, dépendance affective, perte de repères…) qui accepte également des
   **soumissions anonymes** (idée inspirée de sites de contenu comme
   [La Rotonde](https://www.larotonde.ca/) pour la partie articles).

> Mots sur Maux s'inscrit dans une approche de prévention, d'humanisation et
> d'éducation émotionnelle, **sans prétendre remplacer les services de santé
> mentale professionnels.**

## Stack technique

- **Langage : Python 3.11+**
- **Cadre : Django 5.2 (LTS)** — pages rendues côté serveur (bon pour le SEO et
  la simplicité), templates Django.
- **Base de données :** SQLite (développement).
- **Images :** Pillow.
- **Style :** CSS pur (aucune dépendance JS), palette vert forêt + crème inspirée
  du document de présentation.

## Structure du projet

```
config/        Réglages, URLs racine, WSGI/ASGI
core/          Accueil, présentation du projet, contact, branding (context processor)
blog/          La plateforme en ligne : catégories + articles (comme un journal)
submissions/   Les soumissions anonymes (« mettre des mots sur ses maux »)
workshops/     Les ateliers en présentiel + demandes d'atelier des organismes
templates/     Gabarits HTML (base + pages + partiels)
static/css/    Feuille de styles
```

## Démarrage rapide

```bash
# 1. Environnement virtuel (recommandé)
python -m venv .venv && source .venv/bin/activate

# 2. Dépendances
pip install -r requirements.txt

# 3. Base de données
python manage.py migrate

# 4. Données de démonstration (catégories, articles, ateliers)
python manage.py seed_data

# 5. Compte administrateur (pour /admin)
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Le site est alors disponible sur http://127.0.0.1:8000/ et
l'administration sur http://127.0.0.1:8000/admin/.

## Pages principales

| URL                | Description                                        |
|--------------------|----------------------------------------------------|
| `/`                | Accueil (vitrine, articles à la une, deux volets)  |
| `/le-projet/`      | Présentation du projet (mission, vision, volets)   |
| `/articles/`       | La plateforme : liste des articles + filtres       |
| `/articles/<slug>/`| Article                                            |
| `/ateliers/`       | Ateliers à venir + passés                          |
| `/ateliers/demande/`| Formulaire de demande d'atelier (écoles, organismes)|
| `/soumettre/`      | Formulaire de soumission anonyme                   |
| `/contact/`        | Formulaire de contact                              |
| `/admin/`          | Administration (gestion du contenu)                |

## Configuration (variables d'environnement)

| Variable                      | Défaut (dév)                  |
|-------------------------------|-------------------------------|
| `DJANGO_SECRET_KEY`           | clé de développement intégrée |
| `DJANGO_DEBUG`                | `True`                        |
| `DJANGO_ALLOWED_HOSTS`        | `localhost,127.0.0.1,0.0.0.0` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | *(vide)*                      |

## Note sur les fichiers audio

Trois enregistrements audio ont été fournis avec la maquette. Ils **n'ont pas
encore pu être transcrits** dans l'environnement d'exécution actuel (l'accès
réseau y bloque les hôtes d'hébergement de modèles de transcription). Le contenu
de cette première version s'appuie donc sur les diapositives de présentation
fournies et sur la référence visuelle demandée. Les précisions contenues dans
les audios pourront être intégrées dans une prochaine itération.
