from django.urls import path

from . import views

app_name = "workshops"

urlpatterns = [
    path("", views.workshop_list, name="list"),
    path("demande/", views.request_workshop, name="request"),
    path("<slug:slug>/", views.workshop_detail, name="detail"),
]
