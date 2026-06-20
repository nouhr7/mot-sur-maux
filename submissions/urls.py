from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.submit, name="submit"),
    path("merci/", views.merci, name="merci"),
]
