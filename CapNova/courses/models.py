from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Subject(models.Model):
    """Subject/competency area, e.g. 'Numerical Weather Prediction'.
    Used for competency mapping: which trainers are qualified to teach it,
    and which courses fall under it."""

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="courses")
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="courses_taught", limit_choices_to={"role": "trainer"},
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def enrolled_count(self):
        return self.enrollments.count()


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        DROPPED = "dropped", "Dropped"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    trainee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="enrollments", limit_choices_to={"role": "trainee"},
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("course", "trainee")
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.trainee} -> {self.course}"


class LearningResource(models.Model):
    """Trainer library: recorded lectures, presentations, and study
    materials, uploaded by a trainer and visible to enrolled trainees."""

    class ResourceType(models.TextChoices):
        VIDEO = "video", "Recorded lecture"
        SLIDES = "slides", "Presentation"
        DOCUMENT = "document", "Study material"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="resources")
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="uploaded_resources", limit_choices_to={"role": "trainer"},
    )
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    file = models.FileField(upload_to="library/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name="certificate")
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.certificate_number


class Feedback(models.Model):
    """Trainee feedback on a course/training content."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="feedback_entries")
    trainee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="feedback_given", limit_choices_to={"role": "trainee"},
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "trainee")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.trainee} rated {self.course} ({self.rating}/5)"
