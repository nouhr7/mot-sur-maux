"""Small template helpers for the Mots sur Maux site."""

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static as static_url

register = template.Library()


@register.simple_tag
def static_if_exists(path):
    """Return the static URL for *path* only if the file actually exists.

    Lets templates reference optional, drop-in assets (e.g. founder photos at
    static/img/founders/founder-1.jpg) without showing a broken image when the
    file has not been added yet.
    """
    if finders.find(path):
        return static_url(path)
    return ""
