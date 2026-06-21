from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SubmissionForm


def submit(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            # If a member is logged in, keep it in their private history.
            # Moderation stays anonymous (the team views never show the owner).
            if request.user.is_authenticated:
                submission.owner = request.user
            submission.save()
            messages.success(
                request,
                "Merci d'avoir mis des mots sur ce que tu vis. Ton message a "
                "bien été reçu, en toute confidentialité.",
            )
            return redirect(reverse("submissions:merci"))
    else:
        # Optionally pre-fill from a member's journal entry ("partager ce texte").
        initial = {}
        journal_id = request.GET.get("journal")
        if journal_id and request.user.is_authenticated:
            from accounts.models import JournalEntry

            entry = JournalEntry.objects.filter(
                pk=journal_id, user=request.user
            ).first()
            if entry:
                initial["message"] = entry.content
        form = SubmissionForm(initial=initial)

    return render(request, "submissions/submit.html", {"form": form})


def merci(request):
    return render(request, "submissions/merci.html")
