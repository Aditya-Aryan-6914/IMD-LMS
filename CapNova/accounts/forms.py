from django import forms
from django.contrib.auth import password_validation

from .models import TraineeProfile, TrainerProfile, User


class RegisterForm(forms.ModelForm):
    """
    Backs all three tabs on the register page (Trainer / Trainee / Public
    User). `category` comes from the hidden #category-input field the JS
    tab-switcher maintains, and drives which fields are required and what
    role/flags get set on save().
    """

    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "full_name",
            "employee_id",
            "email",
            "phone",
            "institute_name",
            "graduation_year",
        ]

    def __init__(self, *args, category="trainer", **kwargs):
        self.category = category
        super().__init__(*args, **kwargs)
        for name in ("employee_id", "institute_name", "graduation_year"):
            self.fields[name].required = False

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        if employee_id and User.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("This Employee ID is already registered.")
        return employee_id

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm = cleaned.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match.")
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as exc:
                self.add_error("password", exc)

        if self.category == "public":
            if not cleaned.get("institute_name"):
                self.add_error("institute_name", "Institute name is required.")
            if not cleaned.get("graduation_year"):
                self.add_error("graduation_year", "Year of graduation is required.")
        else:
            if not cleaned.get("employee_id"):
                self.add_error("employee_id", "Employee ID is required.")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if self.category == "public":
            user.role = User.Role.TRAINEE
            user.is_public_user = True
            user.employee_id = None
            # Public participants are lower-risk / self-serve: auto-approved.
            user.is_approved = True
        elif self.category == "trainee":
            user.role = User.Role.TRAINEE
            user.is_public_user = False
            user.is_approved = False
        else:  # trainer
            user.role = User.Role.TRAINER
            user.is_public_user = False
            user.is_approved = False

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class TraineeProfileForm(forms.ModelForm):
    class Meta:
        model = TraineeProfile
        fields = ["qualifications", "work_experience", "interests", "skills", "profile_photo"]


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ["designation", "specialization", "bio", "profile_photo", "subjects"]
