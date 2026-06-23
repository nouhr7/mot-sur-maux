# Mettre le site en ligne (accessible 24/7)

Pour que votre ami·e accède au site **même quand votre ordinateur est éteint**,
il faut héberger l'application sur un **serveur dans le nuage** (le cloud), qui
tourne en permanence. `ngrok` ne suffit pas : il ne fait que rediriger vers
**votre** machine — dès qu'elle dort ou se ferme, le lien meurt.

Ce projet est une application **Django**. À éviter : **Vercel / Netlify**
(faits pour des sites « frontend », ils perdraient votre base de données).

> ℹ️ Le code est déjà prêt pour le déploiement (gunicorn, WhiteNoise pour les
> fichiers statiques, base de données configurable, domaines d'hébergement
> autorisés, réglages de sécurité). Vous n'avez **pas** à toucher au code.

> ⚠️ **Votre compte n'est pas sur GitHub.** Le fichier `db.sqlite3` (qui
> contient le compte que vous avez créé) est ignoré par git. Sur un serveur
> neuf, la base démarre **vide**. Deux choix : **téléverser votre `db.sqlite3`**
> pour tout garder (Option A, étape 6), ou **recréer le compte** en une commande.

---

## Option A — PythonAnywhere ⭐ (recommandé : gratuit, toujours en ligne, garde votre compte)

C'est l'option la plus simple pour votre besoin : le site reste joignable en
permanence, et vous pouvez **téléverser votre base actuelle** pour conserver le
compte et le contenu déjà créés.

### 1. Créer le compte
Inscrivez-vous gratuitement sur **https://www.pythonanywhere.com** (compte
« Beginner », sans carte de crédit). Votre site sera à
`https://VOTRENOM.pythonanywhere.com`.

### 2. Récupérer le code (console Bash)
Onglet **Consoles → Bash**, puis :
```bash
git clone https://github.com/nouhr7/mot-sur-maux.git
cd mot-sur-maux
git checkout claude/hopeful-maxwell-sojveh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```

### 3. Créer l'application web
Onglet **Web → Add a new web app → Manual configuration → Python 3.10** (ou la
version proposée).

### 4. Indiquer le virtualenv
Dans la section **Virtualenv** de l'onglet Web, entrez :
```
/home/VOTRENOM/mot-sur-maux/.venv
```

### 5. Configurer le fichier WSGI
Cliquez sur le lien du **fichier WSGI** (section *Code*). Effacez tout et
remplacez par (en mettant **votre** nom d'utilisateur) :
```python
import os
import sys

path = "/home/VOTRENOM/mot-sur-maux"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
os.environ["DJANGO_DEBUG"] = "0"
os.environ["DJANGO_SECRET_KEY"] = "COLLEZ-UNE-LONGUE-CHAINE-ALEATOIRE-ICI"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Pour générer une clé secrète, lancez dans la console Bash :
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
…et collez le résultat à la place de `COLLEZ-UNE-LONGUE-CHAINE-ALEATOIRE-ICI`.

### 6. (Pour garder votre compte) téléverser votre base
Onglet **Files** → ouvrez le dossier `mot-sur-maux/` → **Upload a file** →
envoyez votre `db.sqlite3` local (il remplace la base vide). De retour dans la
console Bash : `python manage.py migrate` (par sécurité).

*Sinon*, pour repartir d'une base vide, créez simplement un identifiant :
```bash
python manage.py creer_membre_equipe nouhr --prenom Nouhr   # accès /equipe/
python manage.py seed_data                                   # (facultatif) contenu de démo
```

### 7. (Pour afficher les images téléversées) ajouter deux mappings de fichiers
Dans l'onglet **Web → Static files**, ajoutez :

| URL | Directory |
|---|---|
| `/static/` | `/home/VOTRENOM/mot-sur-maux/staticfiles` |
| `/media/`  | `/home/VOTRENOM/mot-sur-maux/media` |

### 8. Mettre en ligne
Cliquez le gros bouton vert **Reload**. C'est en ligne :
`https://VOTRENOM.pythonanywhere.com` — le lien à envoyer à votre ami·e. 🎉

> 💡 Sur l'offre gratuite, reconnectez-vous une fois tous les ~3 mois et cliquez
> « Run until 3 months from today » pour garder l'app active.

### Pour mettre à jour le site plus tard
Console Bash :
```bash
cd mot-sur-maux && git pull && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```
…puis **Reload** dans l'onglet Web.

---

## Option B — Render (déploiement automatique depuis GitHub)

Plus automatisé (se redéploie à chaque `git push`), mais : le service gratuit
« s'endort » après 15 min (réveil ~30–60 s) et utilise une base PostgreSQL
(vous **recréez** donc le compte, vous ne pouvez pas téléverser votre SQLite).

1. Compte gratuit sur **https://render.com** (connexion avec GitHub).
2. **New + → Blueprint** → dépôt `nouhr7/mot-sur-maux`, branche
   `claude/hopeful-maxwell-sojveh`. Render lit `render.yaml` et crée le site +
   une base PostgreSQL. **Apply**.
3. Une fois en ligne : onglet **Shell** →
   `python manage.py creer_membre_equipe nouhr --prenom Nouhr`.
4. Adresse : `https://mots-sur-maux.onrender.com`.

Images téléversées non conservées entre redéploiements (disque éphémère) —
stockage objet (Cloudinary/S3) à brancher plus tard.

---

## Récapitulatif

| Besoin | Option |
|---|---|
| **Toujours en ligne, gratuit, garder le compte créé** | **PythonAnywhere** ⭐ |
| Déploiement auto à chaque `git push` | Render |
| Partage de 5 min depuis SON ordinateur allumé | `ngrok` (rien si le PC est éteint) |
