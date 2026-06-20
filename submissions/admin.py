from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "topic", "status", "has_email", "created_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("topic", "feeling", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

    @admin.display(boolean=True, description="Souhaite une réponse")
    def has_email(self, obj):
        return bool(obj.contact_email)
