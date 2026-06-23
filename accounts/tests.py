from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Author, Category
from submissions.models import Submission

from .models import ArticleRead, Bookmark, JournalEntry, Profile

User = get_user_model()


class PasswordResetTests(TestCase):
    def test_reset_sends_email_with_link(self):
        User.objects.create_user("mia", email="mia@example.com", password="old-pw")
        resp = self.client.post(
            reverse("accounts:password_reset"), {"email": "mia@example.com"}
        )
        self.assertRedirects(resp, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/compte/mot-de-passe/", mail.outbox[0].body)

    def test_login_page_offers_reset(self):
        html = self.client.get(reverse("accounts:login")).content.decode()
        self.assertIn(reverse("accounts:password_reset"), html)


class ProfileSignalTests(TestCase):
    def test_profile_created_with_user(self):
        user = User.objects.create_user("alice", password="pw")
        self.assertTrue(Profile.objects.filter(user=user).exists())


class AccountAccessTests(TestCase):
    def test_signup_creates_account_and_logs_in(self):
        resp = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newbie",
                "first_name": "Sam",
                "password1": "motdepasse-solide-1",
                "password2": "motdepasse-solide-1",
            },
        )
        self.assertRedirects(resp, reverse("accounts:dashboard"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp.url)

    def test_site_usable_anonymously(self):
        # A core promise: no account needed to read or submit.
        self.assertEqual(self.client.get(reverse("submissions:submit")).status_code, 200)


class MemberFeatureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mia", password="pw")
        self.client.login(username="mia", password="pw")
        self.category = Category.objects.create(name="Anxiété")
        self.author = Author.objects.create(name="Collectif")
        self.article = Article.objects.create(
            title="Respirer", category=self.category, author=self.author,
            excerpt="x", content="<p>texte</p>", is_published=True,
        )

    def test_journal_entry_is_private_to_owner(self):
        self.client.post(
            reverse("accounts:journal_create"),
            {"title": "Mon texte", "content": "Des mots pour moi."},
        )
        entry = JournalEntry.objects.get(title="Mon texte")
        self.assertEqual(entry.user, self.user)
        # Another member cannot open it.
        User.objects.create_user("bob", password="pw")
        other = self.client.__class__()
        other.login(username="bob", password="pw")
        self.assertEqual(
            other.get(reverse("accounts:journal_edit", args=[entry.pk])).status_code,
            404,
        )

    def test_reading_an_article_records_history(self):
        self.client.get(self.article.get_absolute_url())
        self.assertTrue(
            ArticleRead.objects.filter(user=self.user, article=self.article).exists()
        )

    def test_bookmark_toggle(self):
        url = reverse("accounts:bookmark_toggle", args=[self.article.id])
        self.client.post(url)
        self.assertTrue(Bookmark.objects.filter(user=self.user, article=self.article).exists())
        self.client.post(url)
        self.assertFalse(Bookmark.objects.filter(user=self.user, article=self.article).exists())

    def test_submission_is_linked_to_logged_in_member(self):
        self.client.post(
            reverse("submissions:submit"),
            {"topic": "solitude", "feeling": "", "message": "Je partage.", "contact_email": "", "website": ""},
        )
        sub = Submission.objects.get(topic="solitude")
        self.assertEqual(sub.owner, self.user)

    def test_change_password(self):
        self.client.post(
            reverse("accounts:settings"),
            {
                "change_password": "1",
                "old_password": "pw",
                "new_password1": "tout-nouveau-mdp-7",
                "new_password2": "tout-nouveau-mdp-7",
            },
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("tout-nouveau-mdp-7"))


class StaffProfileTests(TestCase):
    def test_staff_can_update_name_via_profile_page(self):
        User.objects.create_user("redac", password="pw", is_staff=True)
        self.client.login(username="redac", password="pw")
        resp = self.client.post(
            reverse("team:profile"),
            {"save_profile": "1", "first_name": "Nouhr"},
        )
        self.assertRedirects(resp, reverse("team:profile"))
        self.assertEqual(User.objects.get(username="redac").first_name, "Nouhr")


class AccessControlTests(TestCase):
    """Broken Access Control / IDOR regressions — enforcement is server-side."""

    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pw")
        self.bob = User.objects.create_user("bob", password="pw")
        self.cat = Category.objects.create(name="Anxiété")
        self.author = Author.objects.create(name="Collectif")
        self.published = Article.objects.create(
            title="Publié", category=self.cat, author=self.author,
            excerpt="x", content="<p>x</p>", is_published=True,
        )
        self.draft = Article.objects.create(
            title="Brouillon", category=self.cat, author=self.author,
            excerpt="x", content="<p>x</p>", is_published=False,
        )

    def test_cannot_delete_another_members_journal(self):
        entry = JournalEntry.objects.create(user=self.alice, content="privé")
        self.client.login(username="bob", password="pw")
        resp = self.client.post(reverse("accounts:journal_delete", args=[entry.pk]))
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(JournalEntry.objects.filter(pk=entry.pk).exists())

    def test_cannot_open_another_members_journal(self):
        entry = JournalEntry.objects.create(user=self.alice, content="privé")
        self.client.login(username="bob", password="pw")
        self.assertEqual(
            self.client.get(reverse("accounts:journal_edit", args=[entry.pk])).status_code,
            404,
        )

    def test_member_sees_only_own_submissions(self):
        Submission.objects.create(message="confidentiel", owner=self.alice, topic="alice-topic")
        self.client.login(username="bob", password="pw")
        html = self.client.get(reverse("accounts:submission_list")).content.decode()
        self.assertNotIn("alice-topic", html)

    def test_bookmark_toggle_rejects_get(self):
        self.client.login(username="alice", password="pw")
        resp = self.client.get(reverse("accounts:bookmark_toggle", args=[self.published.id]))
        self.assertEqual(resp.status_code, 405)

    def test_cannot_bookmark_unpublished_article(self):
        self.client.login(username="alice", password="pw")
        resp = self.client.post(reverse("accounts:bookmark_toggle", args=[self.draft.id]))
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(
            Bookmark.objects.filter(user=self.alice, article=self.draft).exists()
        )

    def test_can_remove_bookmark_even_if_article_unpublished(self):
        Bookmark.objects.create(user=self.alice, article=self.draft)
        self.client.login(username="alice", password="pw")
        self.client.post(reverse("accounts:bookmark_toggle", args=[self.draft.id]))
        self.assertFalse(
            Bookmark.objects.filter(user=self.alice, article=self.draft).exists()
        )

    def test_anonymous_redirected_from_member_pages(self):
        for name in [
            "accounts:dashboard", "accounts:journal_list", "accounts:bookmark_list",
            "accounts:read_list", "accounts:submission_list", "accounts:settings",
        ]:
            with self.subTest(page=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 302)
                self.assertIn(reverse("accounts:login"), resp.url)
