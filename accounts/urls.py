from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"

urlpatterns = [
    # Authentification des membres
    path(
        "connexion/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("inscription/", views.signup, name="signup"),

    # Réinitialisation du mot de passe (par courriel)
    path(
        "mot-de-passe/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "mot-de-passe/envoye/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "mot-de-passe/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "mot-de-passe/termine/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # Mon espace
    path("", views.dashboard, name="dashboard"),

    # Journal privé
    path("journal/", views.journal_list, name="journal_list"),
    path("journal/nouveau/", views.journal_create, name="journal_create"),
    path("journal/<int:pk>/", views.journal_edit, name="journal_edit"),
    path("journal/<int:pk>/supprimer/", views.journal_delete, name="journal_delete"),

    # Favoris
    path("favoris/", views.bookmark_list, name="bookmark_list"),
    path("favoris/<int:article_id>/", views.bookmark_toggle, name="bookmark_toggle"),

    # Lectures
    path("lectures/", views.read_list, name="read_list"),

    # Mes soumissions
    path("mes-soumissions/", views.submission_list, name="submission_list"),

    # Paramètres
    path("parametres/", views.settings_view, name="settings"),
]
