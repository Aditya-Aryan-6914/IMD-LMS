from django.conf import settings
from django.db import models

from courses.models import Course


class Questionnaire(models.Model):
    """Trainer-created questionnaire/assessment with a deadline
    (PS: 'create questionnaires with deadlines')."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questionnaires")
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="questionnaires_created", limit_choices_to={"role": "trainer"},
    )
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.title

    @property
    def is_past_deadline(self):
        from django.utils import timezone

        return timezone.now() > self.deadline


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    """One trainee's attempt at a questionnaire."""

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="attempts")
    trainee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="assessment_attempts", limit_choices_to={"role": "trainee"},
    )
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("questionnaire", "trainee")
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.trainee} - {self.questionnaire} ({self.score}/{self.total})"


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ("attempt", "question")
