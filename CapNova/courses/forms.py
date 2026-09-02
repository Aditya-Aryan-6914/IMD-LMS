from django import forms

from .models import Course, Feedback, LearningResource, Subject


class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ["course", "title", "resource_type", "file"]

    def __init__(self, *args, trainer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if trainer is not None:
            self.fields["course"].queryset = self.fields["course"].queryset.filter(trainer=trainer)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["rating", "comment"]
        widgets = {"rating": forms.NumberInput(attrs={"min": 1, "max": 5})}


class CourseForm(forms.ModelForm):
    """Admin-facing course creation/edit form: assign a subject, a trainer,
    and publish status. (PS: admin 'assigns courses to trainers'.)"""

    class Meta:
        model = Course
        fields = ["subject", "trainer", "title", "description", "is_published"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User

        self.fields["trainer"].queryset = User.objects.filter(role=User.Role.TRAINER).order_by("full_name")
        self.fields["trainer"].required = False


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
