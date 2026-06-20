from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from blog.models import Article
from workshops.models import Workshop

from .forms import ContactForm


def home(request):
    articles = Article.published.select_related("category")
    featured = articles.filter(is_featured=True).first() or articles.first()
    recent = articles.exclude(pk=featured.pk)[:6] if featured else articles[:6]

    upcoming = Workshop.objects.filter(
        is_published=True, starts_at__gte=timezone.now()
    )[:3]

    return render(
        request,
        "core/home.html",
        {
            "featured": featured,
            "recent": recent,
            "upcoming": upcoming,
        },
    )


def projet(request):
    """« Présentation du projet » — la mission, la vision et les deux volets."""
    return render(request, "core/projet.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Merci pour votre message. Nous vous répondrons bientôt."
            )
            return redirect(reverse("core:contact"))
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
