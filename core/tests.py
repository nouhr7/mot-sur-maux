from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Author, Category


class LegalPagesTests(TestCase):
    def test_legal_pages_render(self):
        for name in ["core:confidentialite", "core:conditions"]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_footer_links_present(self):
        html = self.client.get(reverse("core:contact")).content.decode()
        self.assertIn(reverse("core:confidentialite"), html)
        self.assertIn(reverse("core:conditions"), html)


class HelpButtonTests(TestCase):
    def test_floating_help_button_on_public_pages(self):
        html = self.client.get(reverse("core:home")).content.decode()
        self.assertIn("help-fab", html)
        self.assertIn("Aide immédiate", html)
        self.assertIn("tel:988", html)


class ContentWarningTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Anxiété")
        self.author = Author.objects.create(name="Collectif")

    def _article(self, **kwargs):
        defaults = dict(
            category=self.category, author=self.author,
            excerpt="x", content="<p>texte</p>", is_published=True,
        )
        defaults.update(kwargs)
        return Article.objects.create(**defaults)

    def test_warning_shown_when_set(self):
        article = self._article(title="Nuit", content_warning="suicide")
        html = self.client.get(article.get_absolute_url()).content.decode()
        self.assertIn("Avertissement de contenu", html)
        self.assertIn("suicide", html)
        self.assertIn("9-8-8", html)

    def test_no_warning_when_empty(self):
        article = self._article(title="Lumière")
        html = self.client.get(article.get_absolute_url()).content.decode()
        self.assertNotIn("Avertissement de contenu", html)
