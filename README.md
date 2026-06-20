# Mots sur Maux

> Mettre des mots sur ses maux, à travers l'écriture.

**Mots sur Maux** est un projet d'**éducation à l'expression des émotions** : il
invite et guide chacun — et les jeunes en particulier — à mettre des mots sur les
maux qui les traversent. Ce dépôt contient le site web du projet.

Le site présente l'ensemble du projet, structuré autour de ses **deux volets** :

1. **Des ateliers en présentiel** — des ateliers d'écriture guidée auprès des
   jeunes (écoles, camps d'été, organismes communautaires).
2. **Une plateforme en ligne** — un blog d'articles signés par différentes plumes
   (avec **page auteur** cliquable), sur le vécu émotionnel (anxiété, dépendance
   affective, perte de repères…), qui accepte aussi des **soumissions anonymes**.
   La partie articles s'inspire de sites de contenu comme
   [La Rotonde](https://www.larotonde.ca/).

Le site comprend aussi une **présentation du projet** (mission, vision,
fondateurs), une page **Ressources** en santé mentale (lignes d'écoute, centres)
et la possibilité d'**accueillir / réserver un atelier**.

> Mots sur Maux est un projet d'éducation et de prévention. Il **ne remplace pas
> un suivi ni les services de santé mentale professionnels.**

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
core/          Accueil, présentation du projet, contact, fondateurs, partenaires
blog/          La plateforme : catégories + articles + auteurs (pages auteur)
submissions/   Les soumissions anonymes (« mettre des mots sur ses maux »)
workshops/     Les ateliers en présentiel + demandes / réservation d'atelier
resources/     La page Ressources en santé mentale (situations + lignes d'aide)
templates/     Gabarits HTML (base + pages + partiels)
static/css/    Feuille de styles (palette verte)
```

## Démarrage rapide

```bash
# 1. Environnement virtuel (recommandé)
python -m venv .venv && source .venv/bin/activate

# 2. Dépendances
pip install -r requirements.txt

# 3. Base de données
python manage.py migrate

# 4. Données de démonstration (catégories, auteur, articles, ressources)
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
| `/`                  | Accueil (vitrine, articles à la une, deux volets)|
| `/le-projet/`        | Présentation : constat, conviction, fondateurs   |
| `/articles/`         | La plateforme : liste des articles + filtres     |
| `/articles/<slug>/`  | Article (avec encadré auteur)                    |
| `/articles/auteur/<slug>/` | Page de l'auteur (bio + ses articles)      |
| `/ateliers/`         | Ateliers (à venir/passés), réservation, partenaires |
| `/ateliers/demande/` | Formulaire de demande d'atelier                  |
| `/soumettre/`        | Formulaire de soumission anonyme                 |
| `/ressources/`       | Ressources en santé mentale (lignes d'aide)      |
| `/contact/`          | Formulaire de contact                            |
| `/admin/`            | Administration (gestion du contenu)              |

## Configuration (variables d'environnement)

| Variable                      | Défaut (dév)                  |
|-------------------------------|-------------------------------|
| `DJANGO_SECRET_KEY`           | clé de développement intégrée |
| `DJANGO_DEBUG`                | `True`                        |
| `DJANGO_ALLOWED_HOSTS`        | `localhost,127.0.0.1,0.0.0.0` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | *(vide)*                      |

## Contenu & sources

Le contenu et la structure du site reprennent les **trois briefs audio** fournis
par le porteur du projet (transcrits), ainsi que les diapositives de présentation.

### À personnaliser ensuite (via l'admin ou des fichiers)

- **Logo** — déposer `static/img/logo.svg` puis l'activer dans `templates/base.html`
  (un emplacement commenté est prévu). La palette est déjà au **vert**.
- **Fondateurs** — ajouter les fondateur·rices (nom, rôle, bio, photo) dans
  l'admin → ils apparaissent sur `/le-projet/`.
- **Ateliers & partenaires** — à créer dans l'admin au fur et à mesure (aucun
  atelier n'a encore eu lieu : le site affiche un état vide assumé).
- **Ressources** — vérifier / adapter les lignes d'aide à votre région.
- À intégrer quand disponibles : le **document de présentation** du projet et la
  **référence Wix** du système de publication d'articles.
