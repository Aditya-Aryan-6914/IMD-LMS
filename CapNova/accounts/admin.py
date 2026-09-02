from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import TraineeProfile, TrainerProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Admin lets an Admin-role staffer approve pending users and change
    roles -- this is the PS's 'user approval and role management' feature,
    available immediately via /admin/ while a custom in-app UI is built out."""

    model = User
    ordering = ["-date_joined"]
    list_display = ["email", "full_name", "role", "is_approved", "is_public_user", "is_active", "date_joined"]
    list_filter = ["role", "is_approved", "is_public_user", "is_active"]
    search_fields = ["email", "full_name", "employee_id"]
    readonly_fields = ["date_joined", "last_login"]
    actions = ["approve_users"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone", "employee_id")}),
        ("Role & approval", {"fields": ("role", "is_approved", "is_public_user")}),
        ("Public user details", {"fields": ("institute_name", "graduation_year")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "role", "password1", "password2"),
        }),
    )

    @admin.action(description="Approve selected users")
    def approve_users(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} user(s) approved.")


@admin.register(TraineeProfile)
class TraineeProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__full_name", "user__email"]


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "designation"]
    search_fields = ["user__full_name", "user__email"]
    filter_horizontal = ["subjects"]
