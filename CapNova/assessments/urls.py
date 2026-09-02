from django.urls import path

from . import views

urlpatterns = [
    path("assessments/", views.questionnaire_list, name="questionnaire_list"),
    path("assessments/<int:questionnaire_id>/take/", views.take_questionnaire, name="take_questionnaire"),
    path("assessments/result/<int:attempt_id>/", views.questionnaire_result, name="questionnaire_result"),

    path("trainer/assessments/", views.trainer_questionnaires, name="trainer_questionnaires"),
]
