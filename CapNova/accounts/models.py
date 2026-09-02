from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for the email-based User model."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields.setdefault("is_approved", True)
        extra_fields.setdefault("full_name", extra_fields.get("full_name", "Administrator"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Single custom user model for all three PS roles (Trainee, Trainer, Admin).

    "Public User" registrations (external / non-IMD participants) are stored
    as role=TRAINEE with is_public_user=True -- the problem statement only
    defines three roles, so public sign-ups are treated as a trainee subtype
    rather than a fourth role. See handover.md for the reasoning.
    """

    class Role(models.TextChoices):
        TRAINEE = "trainee", "Trainee"
        TRAINER = "trainer", "Trainer"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TRAINEE)

    employee_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)

    is_public_user = models.BooleanField(default=False)
    institute_name = models.CharField(max_length=255, blank=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)

    # PS requirement: "Admin module should provide user approval ... management"
    is_approved = models.BooleanField(
        default=False,
        help_text="Trainer/Trainee (employee) accounts need admin approval before they can log in.",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    def save(self, *args, **kwargs):
        # Admins (created via role management, not self-registration) are
        # always considered approved.
        if self.role == self.Role.ADMIN:
            self.is_approved = True
        super().save(*args, **kwargs)


class TraineeProfile(models.Model):
    """Trainee profile: qualifications, experience, interests, skills, certificates."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainee_profile")
    qualifications = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to="profiles/trainee/", blank=True, null=True)

    def __str__(self):
        return f"Trainee profile: {self.user.full_name}"


class TrainerProfile(models.Model):
    """Trainer profile, plus subject coverage used for competency mapping."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainer_profile")
    designation = models.CharField(max_length=150, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to="profiles/trainer/", blank=True, null=True)

    # Competency mapping: which subjects this trainer is qualified to teach.
    subjects = models.ManyToManyField(
        "courses.Subject", blank=True, related_name="qualified_trainers"
    )

    def __str__(self):
        return f"Trainer profile: {self.user.full_name}"

    @property
    def avg_feedback_rating(self):
        from courses.models import Feedback

        agg = Feedback.objects.filter(course__trainer=self.user).aggregate(
            models.Avg("rating")
        )
        return agg["rating__avg"]
