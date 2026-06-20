from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from core.models import Partner

from .forms import WorkshopRequestForm
from .models import Workshop


def workshop_list(request):
    now = timezone.now()
    published = Workshop.objects.filter(is_published=True)
    return render(
        request,
        "workshops/list.html",
        {
            "upcoming": published.filter(starts_at__gte=now),
            "past": published.filter(starts_at__lt=now).order_by("-starts_at")[:6],
            "partners": Partner.objects.filter(is_active=True),
        },
    )


def workshop_detail(request, slug):
    workshop = get_object_or_404(Workshop, slug=slug, is_published=True)
    return render(request, "workshops/detail.html", {"workshop": workshop})


def request_workshop(request):
    if request.method == "POST":
        form = WorkshopRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Merci ! Votre demande d'atelier a bien été envoyée. "
                "Nous vous reviendrons rapidement.",
            )
            return redirect(reverse("workshops:request"))
    else:
        form = WorkshopRequestForm()
    return render(request, "workshops/request.html", {"form": form})
