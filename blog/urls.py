from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("categorie/<slug:slug>/", views.category_detail, name="category"),
    path("<slug:slug>/", views.article_detail, name="article_detail"),
]
