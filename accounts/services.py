from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import ProfileForm
from .models import Profile


def process_profile_forms(request):
    """Handle the shared "my profile" page (avatar + name, and password).

    Used by both the member settings page and the staff profile page. Returns
    ``(profile_form, password_form, done)`` where ``done`` is ``"profile"``,
    ``"password"`` or ``None``. The calling view decides where to redirect.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile, user=request.user)
    password_form = PasswordChangeForm(request.user)
    done = None

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=profile, user=request.user
            )
            if profile_form.is_valid():
                profile_form.save()
                done = "profile"
        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Keep the user logged in after changing their password.
                update_session_auth_hash(request, user)
                done = "password"

    return profile_form, password_form, done
