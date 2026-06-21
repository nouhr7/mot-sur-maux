from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from blog.models import Article
from submissions.models import Submission

from .forms import JournalEntryForm, SignupForm
from .models import ArticleRead, Bookmark, JournalEntry
from .services import process_profile_forms


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Bienvenue ! Votre espace personnel est prêt.",
            )
            return redirect("accounts:dashboard")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


# ---------------------------------------------------------------------------
# Mon espace
# ---------------------------------------------------------------------------
@login_required
def dashboard(request):
    user = request.user
    entries = JournalEntry.objects.filter(user=user)
    context = {
        "active": "home",
        "entry_count": entries.count(),
        "recent_entries": entries[:3],
        "bookmark_count": Bookmark.objects.filter(user=user).count(),
        "read_count": ArticleRead.objects.filter(user=user).count(),
        "submission_count": Submission.objects.filter(owner=user).count(),
    }
    return render(request, "accounts/dashboard.html", context)


# ---------------------------------------------------------------------------
# Journal privé
# ---------------------------------------------------------------------------
@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user)
    return render(
        request,
        "accounts/journal_list.html",
        {"active": "journal", "entries": entries},
    )


@login_required
def journal_create(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Votre texte est enregistré.")
            return redirect("accounts:journal_list")
    else:
        form = JournalEntryForm()
    return render(
        request,
        "accounts/journal_form.html",
        {"active": "journal", "form": form, "is_new": True},
    )


@login_required
def journal_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Modifications enregistrées.")
            return redirect("accounts:journal_list")
    else:
        form = JournalEntryForm(instance=entry)
    return render(
        request,
        "accounts/journal_form.html",
        {"active": "journal", "form": form, "entry": entry, "is_new": False},
    )


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Texte supprimé.")
        return redirect("accounts:journal_list")
    return render(
        request,
        "accounts/journal_confirm_delete.html",
        {"active": "journal", "entry": entry},
    )


# ---------------------------------------------------------------------------
# Favoris (articles enregistrés)
# ---------------------------------------------------------------------------
@login_required
def bookmark_list(request):
    bookmarks = (
        Bookmark.objects.filter(user=request.user)
        .select_related("article", "article__category", "article__author")
    )
    return render(
        request,
        "accounts/bookmark_list.html",
        {"active": "favoris", "bookmarks": bookmarks},
    )


@login_required
@require_POST
def bookmark_toggle(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, article=article
    )
    if created:
        messages.success(request, "Article ajouté à vos favoris.")
    else:
        bookmark.delete()
        messages.info(request, "Article retiré de vos favoris.")

    nxt = request.POST.get("next")
    if nxt and url_has_allowed_host_and_scheme(
        nxt, allowed_hosts={request.get_host()}
    ):
        return redirect(nxt)
    return redirect(article.get_absolute_url())


# ---------------------------------------------------------------------------
# Lectures (historique)
# ---------------------------------------------------------------------------
@login_required
def read_list(request):
    reads = (
        ArticleRead.objects.filter(user=request.user)
        .select_related("article", "article__category", "article__author")
    )
    return render(
        request,
        "accounts/read_list.html",
        {"active": "lectures", "reads": reads},
    )


# ---------------------------------------------------------------------------
# Mes soumissions
# ---------------------------------------------------------------------------
@login_required
def submission_list(request):
    submissions = Submission.objects.filter(owner=request.user)
    return render(
        request,
        "accounts/submission_list.html",
        {"active": "soumissions", "submissions": submissions},
    )


# ---------------------------------------------------------------------------
# Paramètres (photo + nom + mot de passe)
# ---------------------------------------------------------------------------
@login_required
def settings_view(request):
    profile_form, password_form, done = process_profile_forms(request)
    if done == "profile":
        messages.success(request, "Profil mis à jour.")
        return redirect("accounts:settings")
    if done == "password":
        messages.success(request, "Mot de passe modifié.")
        return redirect("accounts:settings")
    return render(
        request,
        "accounts/settings.html",
        {
            "active": "parametres",
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )
