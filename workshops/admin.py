from django.contrib import admin

from .models import Workshop, WorkshopRequest


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("title", "host_type", "city", "starts_at", "is_published")
    list_filter = ("host_type", "is_published", "starts_at")
    list_editable = ("is_published",)
    search_fields = ("title", "location_name", "city", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "starts_at"


@admin.register(WorkshopRequest)
class WorkshopRequestAdmin(admin.ModelAdmin):
    list_display = (
        "organization_name",
        "host_type",
        "contact_name",
        "city",
        "status",
        "created_at",
    )
    list_filter = ("status", "host_type", "created_at")
    list_editable = ("status",)
    search_fields = ("organization_name", "contact_name", "email", "city")
    readonly_fields = ("created_at",)
