from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "team"

urlpatterns = [
    # Authentification
    path("connexion/", views.TeamLoginView.as_view(), name="login"),
    path(
        "deconnexion/",
        auth_views.LogoutView.as_view(next_page="team:login"),
        name="logout",
    ),

    # Tableau de bord
    path("", views.dashboard, name="dashboard"),

    # Articles
    path("articles/", views.article_list, name="article_list"),
    path("articles/nouveau/", views.article_create, name="article_create"),
    path("articles/<int:pk>/", views.article_edit, name="article_edit"),
    path("articles/<int:pk>/supprimer/", views.article_delete, name="article_delete"),

    # Ateliers
    path("ateliers/", views.workshop_list, name="workshop_list"),
    path("ateliers/nouveau/", views.workshop_create, name="workshop_create"),
    path("ateliers/<int:pk>/", views.workshop_edit, name="workshop_edit"),
    path("ateliers/<int:pk>/supprimer/", views.workshop_delete, name="workshop_delete"),

    # Soumissions anonymes
    path("soumissions/", views.submission_list, name="submission_list"),
    path("soumissions/<int:pk>/", views.submission_detail, name="submission_detail"),

    # Demandes d'atelier
    path("demandes/", views.request_list, name="request_list"),

    # Mon profil
    path("profil/", views.profile, name="profile"),
]
