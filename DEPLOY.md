# Mettre le site en ligne (déploiement)

Ce projet est une application **Django** (base de données, comptes, admin,
téléversement d'images). Quelques notes avant de choisir un hébergeur :

- **Vercel / Netlify : à éviter ici.** Ils sont faits pour des sites
  « frontend » / serverless. Ils réinitialisent la base SQLite et perdent les
  fichiers téléversés à chaque déploiement. Mauvais outil pour Django.
- **Bon choix : un hébergeur Python/Django.** Deux options gratuites ci-dessous.

> ⚠️ **Votre compte n'est PAS sur GitHub.** Le fichier `db.sqlite3` (qui
> contient le compte que vous avez créé) est ignoré par git. Sur un serveur
> neuf, la base démarre vide : il faudra **recréer le compte** (1 commande) ou
> **téléverser votre `db.sqlite3`** (voir Option B).

---

## Option A — Render (recommandé : déploiement automatique depuis GitHub)

1. Créez un compte gratuit sur **https://render.com** (connectez-vous avec GitHub).
2. Cliquez **New + → Blueprint**.
3. Choisissez le dépôt `nouhr7/mot-sur-maux` et la branche
   `claude/hopeful-maxwell-sojveh`.
4. Render lit le fichier **`render.yaml`** et propose de créer :
   - un service web (le site)
   - une base de données PostgreSQL gratuite
   Cliquez **Apply**. Premier déploiement : ~3–5 minutes.
5. Votre site sera en ligne à une adresse du type
   `https://mots-sur-maux.onrender.com` — c'est le lien à envoyer à votre ami·e.

### Créer votre compte sur le serveur (une fois en ligne)
Dans Render : ouvrez le service → onglet **Shell**, puis lancez :

```bash
# Un identifiant pour l'espace équipe (rédaction) :
python manage.py creer_membre_equipe nouhr --prenom Nouhr

# (facultatif) un accès admin Django complet :
python manage.py createsuperuser

# (facultatif) remplir le site avec du contenu de démonstration :
python manage.py seed_data
```

Votre ami·e pourra alors se connecter sur `/equipe/` (équipe) ou `/compte/`
(membre) avec l'identifiant créé.

**Notes Render (offre gratuite) :**
- Le service « s'endort » après 15 min d'inactivité ; la 1re visite suivante
  prend ~30–60 s à se réveiller. Normal.
- Les **images téléversées** (photos de profil, couvertures) ne sont pas
  conservées entre deux redéploiements (disque éphémère). Pour les rendre
  permanentes, on branchera plus tard un stockage objet (Cloudinary / S3).

---

## Option B — PythonAnywhere (le plus simple, garde votre base actuelle)

Avantage : vous pouvez **téléverser votre `db.sqlite3` local** et garder le
compte + le contenu déjà créés.

1. Créez un compte gratuit sur **https://www.pythonanywhere.com**.
2. Onglet **Consoles → Bash** :
   ```bash
   git clone https://github.com/nouhr7/mot-sur-maux.git
   cd mot-sur-maux
   git checkout claude/hopeful-maxwell-sojveh
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --no-input
   ```
3. Onglet **Web → Add a new web app → Manual config (Python 3.x)**.
4. Dans la config WSGI, pointez vers `config.wsgi` et le dossier du projet,
   et le virtualenv `.venv` (PythonAnywhere fournit un modèle à compléter).
5. **Static files** : URL `/static/` → dossier `.../mot-sur-maux/staticfiles`.
6. Variables d'environnement : `DJANGO_DEBUG=0` et
   `DJANGO_ALLOWED_HOSTS=votrenom.pythonanywhere.com`.
7. Pour **garder votre compte** : onglet **Files**, téléversez votre
   `db.sqlite3` local dans le dossier du projet (remplace la base vide).
8. Cliquez **Reload**. Le site est en ligne à
   `https://votrenom.pythonanywhere.com`.

---

## Récapitulatif

| Besoin | Option |
|---|---|
| Déploiement auto à chaque `git push`, moderne | **Render** |
| Le plus simple, et garder le compte/contenu déjà créés | **PythonAnywhere** |
| Partage rapide 5 min depuis SON ordinateur allumé | `ngrok` (ne marche pas si le PC est éteint) |

Quel que soit le choix, le code est déjà prêt (gunicorn, WhiteNoise pour les
fichiers statiques, base de données configurable, réglages de sécurité en
production).
