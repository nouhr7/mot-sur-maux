from django.db.models import Prefetch
from django.shortcuts import render

from .models import Resource, ResourceCategory


def resource_list(request):
    """The mental-health resources page, grouped by situation."""
    categories = ResourceCategory.objects.prefetch_related(
        Prefetch("resources", queryset=Resource.objects.filter(is_active=True))
    )
    # On garde uniquement les situations qui ont au moins une ressource active.
    categories = [c for c in categories if c.resources.all()]
    urgent = [c for c in categories if c.is_urgent]
    others = [c for c in categories if not c.is_urgent]

    return render(
        request,
        "resources/resource_list.html",
        {"urgent": urgent, "others": others},
    )
