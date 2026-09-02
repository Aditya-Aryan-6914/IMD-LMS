from django.conf import settings
from django.db import models


class Announcement(models.Model):
    """PS: 'Admins should also be able to publish notifications,
    announcements, achievements, and newly added learning content on the
    homepage.'"""

    class Kind(models.TextChoices):
        NOTIFICATION = "notification", "Notification"
        ANNOUNCEMENT = "announcement", "Announcement"
        ACHIEVEMENT = "achievement", "Achievement"
        NEW_CONTENT = "new_content", "New learning content"

    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.ANNOUNCEMENT)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        limit_choices_to={"role": "admin"},
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_kind_display()}] {self.title}"
