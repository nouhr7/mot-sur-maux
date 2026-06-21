from .models import Profile


def ensure_profile(sender, instance, created, **kwargs):
    """Give every new user a Profile so templates can rely on user.profile."""
    if created:
        Profile.objects.get_or_create(user=instance)
