from django.contrib import admin

from .models import Resource, ResourceCategory


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_urgent", "order")
    list_editable = ("is_urgent", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ResourceInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "phone", "region", "is_active", "order")
    list_filter = ("category", "is_active", "region")
    list_editable = ("is_active", "order")
    search_fields = ("name", "description", "phone")
