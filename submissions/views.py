from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SubmissionForm


def submit(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Merci d'avoir mis des mots sur ce que tu vis. Ton message a "
                "bien été reçu, en toute confidentialité.",
            )
            return redirect(reverse("submissions:merci"))
    else:
        form = SubmissionForm()

    return render(request, "submissions/submit.html", {"form": form})


def merci(request):
    return render(request, "submissions/merci.html")
