from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "article_count", "color")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "article_count", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name", "role", "bio")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "is_published",
        "is_featured",
        "published_at",
    )
    list_filter = ("is_published", "is_featured", "category", "author", "published_at")
    list_editable = ("is_published", "is_featured")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    autocomplete_fields = ("source_submission",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "author")}),
        ("Contenu", {"fields": ("excerpt", "content")}),
        ("Image", {"fields": ("cover_image", "cover_credit")}),
        (
            "Publication",
            {"fields": ("is_published", "is_featured", "published_at", "source_submission")},
        ),
    )
