from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_router, name="dashboard"),

    path("dashboard/trainee/", views.trainee_dashboard, name="trainee_dashboard"),
    path("dashboard/trainee/profile/", views.trainee_profile_edit, name="trainee_profile_edit"),

    path("dashboard/trainer/", views.trainer_dashboard, name="trainer_dashboard"),
    path("dashboard/trainer/profile/", views.trainer_profile_edit, name="trainer_profile_edit"),

    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/approve/<int:user_id>/", views.approve_user, name="approve_user"),
    path("dashboard/admin/reject/<int:user_id>/", views.reject_user, name="reject_user"),
]
