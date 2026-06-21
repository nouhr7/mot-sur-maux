"""Allow-list HTML sanitiser for the team's visual editor.

The rich-text editor (Quill) produces HTML. Even though only trusted,
authenticated team members can use it, we still sanitise that HTML on save so
that what we store — and later render with ``|safe`` — is limited to a small,
predictable set of tags. No ``<script>``, no inline styles, no event handlers,
no unexpected attributes.

This is intentionally dependency-free (standard library only) so the project
keeps its tiny requirements list.
"""

from html import escape
from html.parser import HTMLParser

# Tags the editor is allowed to emit. Anything else is dropped (its text
# content is kept and escaped, so nothing is executed).
ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "u", "s",
    "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "a",
}
VOID_TAGS = {"br"}
ALLOWED_URL_SCHEMES = ("http://", "https://", "mailto:", "/")


class _Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS:
            return
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if href.startswith(ALLOWED_URL_SCHEMES):
                self.parts.append(
                    '<a href="%s" rel="noopener noreferrer" target="_blank">'
                    % escape(href, quote=True)
                )
            else:
                # Keep the link text, drop the unsafe destination.
                self.parts.append("<a>")
            return
        self.parts.append("<%s>" % tag)

    def handle_startendtag(self, tag, attrs):
        if tag in VOID_TAGS:
            self.parts.append("<%s>" % tag)

    def handle_endtag(self, tag):
        if tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.parts.append("</%s>" % tag)

    def handle_data(self, data):
        self.parts.append(escape(data))


def clean_html(raw):
    """Return a sanitised copy of ``raw`` containing only allow-listed markup."""
    if not raw:
        return ""
    parser = _Sanitizer()
    parser.feed(raw)
    parser.close()
    return "".join(parser.parts).strip()


def strip_tags(raw):
    """Plain-text version of some HTML (used for word counts / previews)."""
    if not raw:
        return ""
    import re

    return re.sub(r"<[^>]+>", " ", raw)
