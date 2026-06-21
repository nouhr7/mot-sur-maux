from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Author, Category
from submissions.models import Submission

from .models import ArticleRead, Bookmark, JournalEntry, Profile

User = get_user_model()


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
