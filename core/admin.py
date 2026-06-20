from django.contrib import admin

from .models import ContactMessage, Founder, Partner


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_handled", "created_at")
    list_filter = ("is_handled", "created_at")
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role", "bio")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name",)


admin.site.site_header = "Mots sur Maux — Administration"
admin.site.site_title = "Mots sur Maux"
admin.site.index_title = "Gestion du site"
