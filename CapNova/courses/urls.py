from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("courses/<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),

    path("trainer/library/", views.trainer_library, name="trainer_library"),

    path("competency-map/", views.competency_map, name="competency_map"),
]
