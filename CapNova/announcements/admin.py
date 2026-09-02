from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "is_published", "posted_by", "created_at"]
    list_filter = ["kind", "is_published"]
    search_fields = ["title", "body"]

    def save_model(self, request, obj, form, change):
        if not obj.posted_by_id:
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)
