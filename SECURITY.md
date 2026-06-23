# Sécurité — posture du site

Résumé de la façon dont *Mots sur Maux* se protège, et de ce qu'il reste à
faire avant une ouverture publique large. Couvre les grandes catégories du
**OWASP Top 10**.

## Ce qui est en place

### A01 — Contrôle d'accès (Broken Access Control)
- Vérifié **côté serveur** sur chaque requête, jamais par l'interface.
- `/equipe/` : chaque vue exige `@team_member_required` (actif + *staff*).
- `/compte/` : chaque vue exige `@login_required`.
- **Propriété des objets** : un membre n'accède qu'à ses propres données — le
  journal/les favoris/l'historique sont filtrés par `user=request.user`, et
  l'édition/suppression d'une entrée passe par
  `get_object_or_404(JournalEntry, pk=pk, user=request.user)` → **404** sinon.
- Les brouillons d'articles renvoient **404** par URL (manager `published`).
- Couvert par des tests de non-régression (un non-staff reçoit 403 même en
  POST direct, un membre ne peut pas ouvrir le journal d'un autre, etc.).

### A03 — Injection
- **SQL** : uniquement via l'ORM Django (requêtes paramétrées) — aucun SQL brut.
- **XSS** : auto-échappement des gabarits Django. Le corps des articles (seul
  HTML « riche ») passe par un **assainisseur à liste blanche** (`team/sanitize.py`)
  **à l'entrée** (formulaire de l'éditeur) **et à la sortie** (`Article.body_html`),
  donc même un HTML collé dans l'admin est neutralisé.
- Aucune exécution de commande (`os.system`, `subprocess`, `eval`…).

### A02 / A05 — Chiffrement & configuration
- Mots de passe hachés par Django (PBKDF2) + validateurs de robustesse.
- En production (`DEBUG=0`) : redirection HTTPS, cookies `Secure`, en-tête de
  proxy SSL.
- En-têtes de sécurité : `X-Content-Type-Options: nosniff`, `X-Frame-Options:
  DENY` (anti-clickjacking), `Referrer-Policy`, cookies `HttpOnly`.
- `SECRET_KEY` et `DEBUG` lus depuis l'environnement (jamais en clair en prod).
- `manage.py check --deploy` ne lève plus qu'un avertissement (HSTS, voir plus bas).

### A07 — Authentification
- Connexions séparées membres / équipe, réinitialisation du mot de passe par
  courriel, validateurs de mot de passe, sessions sécurisées.
- Pièges anti-pourriel (honeypot) sur les formulaires de soumission et de
  demande d'atelier.

### CSRF
- Middleware CSRF actif + jeton `{% csrf_token %}` sur tous les formulaires.
- Actions modifiantes en **POST** uniquement (`@require_POST`, suppressions).
- Garde anti-redirection ouverte sur les paramètres `next`.

## À faire avant l'ouverture publique (recommandé)

1. **Limitation des tentatives (rate limiting)** sur la connexion et
   l'inscription — p. ex. `django-axes` (verrouillage après N échecs).
2. **HSTS** : sur un **domaine personnalisé**, définir
   `DJANGO_HSTS_SECONDS=31536000` (et `…INCLUDE_SUBDOMAINS` / `…PRELOAD` au
   besoin). Laissé désactivé tant qu'on est sur `*.pythonanywhere.com`
   (sous-domaine partagé).
3. **Politique de sécurité du contenu (CSP)** — durcit encore le XSS ; nécessite
   d'ajuster les styles/scripts en ligne (ou des *nonces*).
4. **Service d'envoi de courriels** réel (SMTP) pour que la réinitialisation du
   mot de passe parte vraiment.
5. **Limite de taille des téléversements** d'images, et mises à jour régulières
   des dépendances (Django, Pillow).
6. **Journalisation / supervision** des erreurs en production.

## Signaler un problème
Pour signaler une faille, écrire à l'adresse de contact du site plutôt que
d'ouvrir un ticket public.
