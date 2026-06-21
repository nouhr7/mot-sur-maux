from django import forms as djforms
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from blog.models import Article
from submissions.models import Submission
from workshops.models import Workshop, WorkshopRequest

from .decorators import team_member_required
from .forms import ArticleForm, SubmissionStatusForm, WorkshopForm


# ---------------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------------
class TeamLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise djforms.ValidationError(
                "Ce compte n'a pas encore accès à l'espace équipe. "
                "Contactez la personne responsable du site.",
                code="no_team",
            )


class TeamLoginView(auth_views.LoginView):
    template_name = "team/login.html"
    redirect_authenticated_user = True
    authentication_form = TeamLoginForm


# ---------------------------------------------------------------------------
# Tableau de bord
# ---------------------------------------------------------------------------
@team_member_required
def dashboard(request):
    now = timezone.now()
    articles = Article.objects.all()
    context = {
        "active": "home",
        "draft_count": articles.filter(is_published=False).count(),
        "published_count": articles.filter(is_published=True).count(),
        "upcoming_count": Workshop.objects.filter(
            is_published=True, starts_at__gte=now
        ).count(),
        "new_submissions": Submission.objects.filter(
            status=Submission.Status.NEW
        ).count(),
        "open_requests": WorkshopRequest.objects.filter(
            status=WorkshopRequest.Status.NEW
        ).count(),
        "recent_articles": articles.select_related("category", "author")[:5],
        "recent_submissions": Submission.objects.all()[:4],
    }
    return render(request, "team/dashboard.html", context)


# ---------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------
def _apply_publish_action(article, action):
    """Translate a named submit button into publication state."""
    if action == "publish":
        article.is_published = True
        if not article.published_at:
            article.published_at = timezone.now()
    elif action in ("draft", "unpublish"):
        article.is_published = False
    # action == "save": leave the current state untouched.


@team_member_required
def article_list(request):
    articles = Article.objects.select_related("category", "author").all()
    return render(
        request,
        "team/article_list.html",
        {"active": "articles", "articles": articles},
    )


@team_member_required
def article_create(request):
    submission = None
    sub_id = request.GET.get("from_submission") or request.POST.get("from_submission")
    if sub_id:
        submission = Submission.objects.filter(pk=sub_id).first()

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            _apply_publish_action(article, request.POST.get("action"))
            if submission:
                article.source_submission = submission
            article.save()
            if submission and submission.status == Submission.Status.NEW:
                submission.status = Submission.Status.IN_REVIEW
                submission.save(update_fields=["status"])
            messages.success(
                request,
                "Article publié." if article.is_published
                else "Brouillon enregistré.",
            )
            return redirect("team:article_list")
    else:
        initial = {}
        if submission:
            initial["excerpt"] = (submission.feeling or submission.topic or "")[:300]
            paras = [p.strip() for p in submission.message.split("\n\n") if p.strip()]
            initial["content"] = "".join(
                "<p>%s</p>" % escape(p) for p in paras
            )
        form = ArticleForm(initial=initial)

    return render(
        request,
        "team/article_form.html",
        {"active": "articles", "form": form, "submission": submission, "is_new": True},
    )


@team_member_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            _apply_publish_action(article, request.POST.get("action"))
            article.save()
            messages.success(request, "Modifications enregistrées.")
            return redirect("team:article_list")
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        "team/article_form.html",
        {"active": "articles", "form": form, "article": article, "is_new": False},
    )


@team_member_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article supprimé.")
        return redirect("team:article_list")
    return render(
        request,
        "team/confirm_delete.html",
        {
            "active": "articles",
            "object_label": article.title,
            "kind": "cet article",
            "cancel_url": reverse("team:article_list"),
        },
    )


# ---------------------------------------------------------------------------
# Ateliers
# ---------------------------------------------------------------------------
@team_member_required
def workshop_list(request):
    now = timezone.now()
    workshops = Workshop.objects.all()
    return render(
        request,
        "team/workshop_list.html",
        {
            "active": "ateliers",
            "upcoming": workshops.filter(starts_at__gte=now),
            "past": workshops.filter(starts_at__lt=now).order_by("-starts_at"),
        },
    )


@team_member_required
def workshop_create(request):
    if request.method == "POST":
        form = WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Atelier enregistré.")
            return redirect("team:workshop_list")
    else:
        form = WorkshopForm()
    return render(
        request,
        "team/workshop_form.html",
        {"active": "ateliers", "form": form, "is_new": True},
    )


@team_member_required
def workshop_edit(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    if request.method == "POST":
        form = WorkshopForm(request.POST, request.FILES, instance=workshop)
        if form.is_valid():
            form.save()
            messages.success(request, "Modifications enregistrées.")
            return redirect("team:workshop_list")
    else:
        form = WorkshopForm(instance=workshop)
    return render(
        request,
        "team/workshop_form.html",
        {"active": "ateliers", "form": form, "workshop": workshop, "is_new": False},
    )


@team_member_required
def workshop_delete(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    if request.method == "POST":
        workshop.delete()
        messages.success(request, "Atelier supprimé.")
        return redirect("team:workshop_list")
    return render(
        request,
        "team/confirm_delete.html",
        {
            "active": "ateliers",
            "object_label": workshop.title,
            "kind": "cet atelier",
            "cancel_url": reverse("team:workshop_list"),
        },
    )


# ---------------------------------------------------------------------------
# Soumissions anonymes
# ---------------------------------------------------------------------------
@team_member_required
def submission_list(request):
    submissions = Submission.objects.all()
    return render(
        request,
        "team/submission_list.html",
        {"active": "soumissions", "submissions": submissions},
    )


@team_member_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == "POST":
        form = SubmissionStatusForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Soumission mise à jour.")
            return redirect("team:submission_detail", pk=pk)
    else:
        form = SubmissionStatusForm(instance=submission)
    return render(
        request,
        "team/submission_detail.html",
        {"active": "soumissions", "submission": submission, "form": form},
    )


# ---------------------------------------------------------------------------
# Demandes d'atelier
# ---------------------------------------------------------------------------
@team_member_required
def request_list(request):
    if request.method == "POST":
        obj = get_object_or_404(WorkshopRequest, pk=request.POST.get("pk"))
        status = request.POST.get("status")
        if status in dict(WorkshopRequest.Status.choices):
            obj.status = status
            obj.save(update_fields=["status"])
            messages.success(request, "Statut mis à jour.")
        return redirect("team:request_list")
    return render(
        request,
        "team/request_list.html",
        {
            "active": "demandes",
            "requests": WorkshopRequest.objects.all(),
            "status_choices": WorkshopRequest.Status.choices,
        },
    )
