from django.contrib import admin

from .models import Certificate, Course, Enrollment, Feedback, LearningResource, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "trainer", "is_published", "enrolled_count", "created_at"]
    list_filter = ["is_published", "subject"]
    search_fields = ["title", "trainer__full_name"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["trainee", "course", "status", "enrolled_at"]
    list_filter = ["status", "course"]
    search_fields = ["trainee__full_name", "course__title"]


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "trainer", "resource_type", "uploaded_at"]
    list_filter = ["resource_type", "course"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["certificate_number", "enrollment", "issued_at"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["trainee", "course", "rating", "submitted_at"]
    list_filter = ["rating", "course"]
