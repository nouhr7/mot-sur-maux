from django.test import TestCase
from django.urls import reverse

from .models import Article, Author, Category


class ArticleSearchTests(TestCase):
    def setUp(self):
        self.anx = Category.objects.create(name="Anxiété")
        self.joie = Category.objects.create(name="Joie")
        self.author = Author.objects.create(name="Marie Tremblay")
        self.a1 = Article.objects.create(
            title="Comprendre le stress", category=self.anx, author=self.author,
            excerpt="apprendre à respirer", content="<p>respiration et calme</p>",
            is_published=True,
        )
        self.a2 = Article.objects.create(
            title="La joie simple", category=self.joie, author=self.author,
            excerpt="petits bonheurs", content="<p>lumière du matin</p>",
            is_published=True,
        )

    def _search(self, q):
        return self.client.get(reverse("blog:article_list"), {"q": q})

    def test_search_by_title(self):
        resp = self._search("stress")
        self.assertContains(resp, "Comprendre le stress")
        self.assertNotContains(resp, "La joie simple")

    def test_search_by_content(self):
        self.assertContains(self._search("respiration"), "Comprendre le stress")

    def test_search_by_author(self):
        self.assertContains(self._search("Tremblay"), "Comprendre le stress")

    def test_search_by_theme(self):
        resp = self._search("Anxiété")
        self.assertContains(resp, "Comprendre le stress")
        self.assertNotContains(resp, "La joie simple")

    def test_no_results_message(self):
        self.assertContains(self._search("zzzintrouvable"), "Aucun article ne correspond")

    def test_unpublished_excluded_from_search(self):
        Article.objects.create(
            title="Brouillon secret", category=self.anx, author=self.author,
            excerpt="x", content="<p>x</p>", is_published=False,
        )
        self.assertNotContains(self._search("secret"), "Brouillon secret")

    def test_blank_query_shows_all(self):
        resp = self.client.get(reverse("blog:article_list"))
        self.assertContains(resp, "Comprendre le stress")
        self.assertContains(resp, "La joie simple")


class DraftAccessTests(TestCase):
    """A draft article must not be reachable by URL (no force-browsing)."""

    def setUp(self):
        self.cat = Category.objects.create(name="Anxiété")
        self.author = Author.objects.create(name="Collectif")
        self.draft = Article.objects.create(
            title="Brouillon confidentiel", category=self.cat, author=self.author,
            excerpt="x", content="<p>secret</p>", is_published=False,
        )

    def test_draft_returns_404_by_url(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)

    def test_draft_not_listed(self):
        html = self.client.get(reverse("blog:article_list")).content.decode()
        self.assertNotIn("Brouillon confidentiel", html)
