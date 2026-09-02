from django.shortcuts import render

from .models import Announcement


def home(request):
    """Public homepage: latest published announcements/notifications/
    achievements/new content, per the PS's homepage requirement."""
    announcements = Announcement.objects.filter(is_published=True)[:10]
    return render(request, "home.html", {"announcements": announcements})
