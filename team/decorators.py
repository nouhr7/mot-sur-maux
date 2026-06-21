from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def team_member_required(view):
    """Allow only active staff users into the Espace équipe.

    A « membre de l'équipe » is simply an active user with the *staff* flag.
    The site creator decides who that is (via the admin or the
    ``creer_membre_equipe`` management command). Visitors who are not logged in
    are sent to the friendly login page; logged-in users without access get a
    clear 403.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not (user.is_active and user.is_staff):
            raise PermissionDenied(
                "Ce compte n'a pas accès à l'espace équipe."
            )
        return view(request, *args, **kwargs)

    return wrapper
