"""URL configuration for the Mots sur Maux project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("articles/", include("blog.urls")),
    path("ateliers/", include("workshops.urls")),
    path("soumettre/", include("submissions.urls")),
    path("ressources/", include("resources.urls")),
]

# Sert les fichiers téléversés (images) pendant le développement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
