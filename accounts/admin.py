from django.contrib import admin

from .models import ArticleRead, Bookmark, JournalEntry, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email", "user__first_name")


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("display_title", "user", "updated_at")
    search_fields = ("title", "user__username")
    list_filter = ("updated_at",)
    # Le journal est privé : lecture seule côté admin, pour le respect.
    readonly_fields = ("user", "title", "content", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")


@admin.register(ArticleRead)
class ArticleReadAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "read_at")
