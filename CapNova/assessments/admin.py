from django.contrib import admin

from .models import Attempt, AttemptAnswer, Choice, Question, Questionnaire


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "trainer", "deadline", "is_past_deadline"]
    list_filter = ["course"]
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "questionnaire", "order"]
    inlines = [ChoiceInline]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ["trainee", "questionnaire", "score", "total", "submitted_at"]
    list_filter = ["questionnaire"]


admin.site.register(AttemptAnswer)
