from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("le-projet/", views.projet, name="projet"),
    path("confidentialite/", views.confidentialite, name="confidentialite"),
    path("conditions/", views.conditions, name="conditions"),
    path("contact/", views.contact, name="contact"),
]
