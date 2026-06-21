from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Author, Category
from submissions.models import Submission
from workshops.models import Workshop, WorkshopRequest

from .sanitize import clean_html


class SanitizerTests(TestCase):
    def test_keeps_allowed_markup(self):
        html = clean_html("<p>Bonjour <strong>monde</strong> et <em>vous</em>.</p>")
        self.assertEqual(
            html, "<p>Bonjour <strong>monde</strong> et <em>vous</em>.</p>"
        )

    def test_drops_scripts_and_unknown_tags(self):
        html = clean_html("<p>ok</p><script>alert(1)</script><div>x</div>")
        self.assertNotIn("<script", html)
        self.assertNotIn("<div", html)
        self.assertIn("<p>ok</p>", html)

    def test_neutralises_javascript_links(self):
        html = clean_html('<a href="javascript:evil()">clic</a>')
        self.assertNotIn("javascript:", html)
        self.assertIn("clic", html)

    def test_keeps_safe_links_with_rel(self):
        html = clean_html('<a href="https://exemple.org">lien</a>')
        self.assertIn('href="https://exemple.org"', html)
        self.assertIn("noopener", html)


class TeamAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user("redac", password="pw", is_staff=True)
        self.visitor = User.objects.create_user("public", password="pw")

    def test_anonymous_redirected_to_login(self):
        resp = self.client.get(reverse("team:dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("team:login"), resp.url)

    def test_non_staff_forbidden(self):
        self.client.login(username="public", password="pw")
        self.assertEqual(self.client.get(reverse("team:dashboard")).status_code, 403)

    def test_staff_can_open_dashboard(self):
        self.client.login(username="redac", password="pw")
        self.assertEqual(self.client.get(reverse("team:dashboard")).status_code, 200)


class HeaderEntryTests(TestCase):
    """The friendly access points shown in the public site header."""

    def _header(self, **login):
        if login:
            self.client.login(**login)
        return self.client.get(reverse("submissions:submit")).content.decode()

    def test_staff_sees_team_entrance(self):
        User = get_user_model()
        User.objects.create_user("redac", password="pw", is_staff=True)
        html = self._header(username="redac", password="pw")
        # The header button is marked with the brand-staff-link class.
        self.assertIn("brand-staff-link", html)
        self.assertIn("Espace équipe", html)

    def test_member_sees_personal_space(self):
        User = get_user_model()
        User.objects.create_user("mia", password="pw")
        html = self._header(username="mia", password="pw")
        self.assertIn(reverse("accounts:dashboard"), html)
        self.assertNotIn("brand-staff-link", html)

    def test_anonymous_sees_login(self):
        html = self._header()
        self.assertIn(reverse("accounts:login"), html)
        self.assertNotIn("brand-staff-link", html)


class TeamWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user("redac", password="pw", is_staff=True)
        self.client.login(username="redac", password="pw")
        self.category = Category.objects.create(name="Anxiété")
        self.author = Author.objects.create(name="Collectif Mots sur Maux")

    def test_publish_article_sanitises_and_shows_online(self):
        resp = self.client.post(
            reverse("team:article_create"),
            {
                "title": "Respirer par les mots",
                "category": self.category.pk,
                "author": self.author.pk,
                "excerpt": "Un court résumé.",
                "content": "<p>Texte <strong>fort</strong>.</p>"
                           "<script>alert(1)</script>",
                "action": "publish",
            },
        )
        self.assertRedirects(resp, reverse("team:article_list"))
        article = Article.objects.get(title="Respirer par les mots")
        self.assertTrue(article.is_published)
        self.assertNotIn("<script", article.content)
        self.assertIn("<strong>fort</strong>", article.content)
        # Visible on the public site, rendered as safe HTML.
        page = self.client.get(article.get_absolute_url())
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "<strong>fort</strong>")

    def test_draft_button_keeps_article_hidden(self):
        self.client.post(
            reverse("team:article_create"),
            {
                "title": "Brouillon",
                "category": self.category.pk,
                "author": self.author.pk,
                "excerpt": "x",
                "content": "<p>en cours</p>",
                "action": "draft",
            },
        )
        self.assertFalse(Article.objects.get(title="Brouillon").is_published)

    def test_create_article_from_submission(self):
        sub = Submission.objects.create(topic="solitude", message="Je me sens seul.")
        resp = self.client.post(
            reverse("team:article_create") + f"?from_submission={sub.pk}",
            {
                "from_submission": sub.pk,
                "title": "Sur la solitude",
                "category": self.category.pk,
                "author": self.author.pk,
                "excerpt": "x",
                "content": "<p>texte</p>",
                "action": "publish",
            },
        )
        self.assertRedirects(resp, reverse("team:article_list"))
        article = Article.objects.get(title="Sur la solitude")
        self.assertEqual(article.source_submission_id, sub.pk)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Submission.Status.IN_REVIEW)

    def test_create_workshop(self):
        resp = self.client.post(
            reverse("team:workshop_create"),
            {
                "title": "Atelier découverte",
                "host_type": "school",
                "location_name": "École des Sources",
                "city": "Montréal",
                "audience": "12-17 ans",
                "description": "Un bel atelier.",
                "starts_at": "2030-05-12T18:00",
                "registration_url": "",
                "is_published": "on",
            },
        )
        self.assertRedirects(resp, reverse("team:workshop_list"))
        self.assertTrue(Workshop.objects.filter(title="Atelier découverte").exists())

    def test_update_submission_status(self):
        sub = Submission.objects.create(message="…")
        self.client.post(
            reverse("team:submission_detail", args=[sub.pk]),
            {"status": Submission.Status.ARCHIVED, "moderator_notes": "Traité."},
        )
        sub.refresh_from_db()
        self.assertEqual(sub.status, Submission.Status.ARCHIVED)

    def test_update_request_status(self):
        req = WorkshopRequest.objects.create(
            organization_name="Camp Soleil", contact_name="A", email="a@b.ca"
        )
        self.client.post(
            reverse("team:request_list"),
            {"pk": req.pk, "status": WorkshopRequest.Status.SCHEDULED},
        )
        req.refresh_from_db()
        self.assertEqual(req.status, WorkshopRequest.Status.SCHEDULED)
