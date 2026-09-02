from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("courses/<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),

    path("trainer/library/", views.trainer_library, name="trainer_library"),

    path("competency-map/", views.competency_map, name="competency_map"),

    path("dashboard/admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("dashboard/admin/courses/new/", views.admin_course_create, name="admin_course_create"),
    path("dashboard/admin/courses/<int:course_id>/edit/", views.admin_course_edit, name="admin_course_edit"),
    path(
        "dashboard/admin/courses/<int:course_id>/toggle-publish/",
        views.admin_course_toggle_publish, name="admin_course_toggle_publish",
    ),
    path(
        "dashboard/admin/courses/<int:course_id>/delete/",
        views.admin_course_delete, name="admin_course_delete",
    ),
    path("dashboard/admin/subjects/new/", views.admin_subject_create, name="admin_subject_create"),

    path(
        "trainer/courses/<int:course_id>/enrollments/",
        views.trainer_course_enrollments, name="trainer_course_enrollments",
    ),
    path(
        "trainer/enrollments/<int:enrollment_id>/complete/",
        views.mark_enrollment_complete, name="mark_enrollment_complete",
    ),
    path("certificates/<int:certificate_id>/download/", views.download_certificate, name="download_certificate"),
    path("certificates/verify/<str:certificate_number>/", views.verify_certificate, name="verify_certificate"),
]
