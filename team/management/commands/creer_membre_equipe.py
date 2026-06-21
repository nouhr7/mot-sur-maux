import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Crée (ou met à jour) un membre de l'équipe ayant accès à l'espace "
        "de rédaction /equipe/. Aucun accès à l'admin Django n'est requis."
    )

    def add_arguments(self, parser):
        parser.add_argument("username", help="Identifiant de connexion")
        parser.add_argument("--email", default="", help="Courriel (facultatif)")
        parser.add_argument(
            "--prenom", default="", help="Prénom affiché dans le tableau de bord"
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        user, created = User.objects.get_or_create(username=username)
        if options["email"]:
            user.email = options["email"]
        if options["prenom"]:
            user.first_name = options["prenom"]
        user.is_staff = True
        user.is_active = True

        if created:
            password = getpass.getpass("Mot de passe : ")
            confirm = getpass.getpass("Confirmez le mot de passe : ")
            if password != confirm:
                raise CommandError("Les mots de passe ne correspondent pas.")
            if not password:
                raise CommandError("Le mot de passe ne peut pas être vide.")
            user.set_password(password)
        else:
            answer = input(
                "Cet identifiant existe déjà. Réinitialiser le mot de passe ? [o/N] "
            )
            if answer.strip().lower() in {"o", "oui", "y", "yes"}:
                password = getpass.getpass("Nouveau mot de passe : ")
                if password:
                    user.set_password(password)

        user.save()

        verb = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"Membre de l'équipe « {username} » {verb}. "
                "Il peut se connecter sur /equipe/connexion/."
            )
        )
