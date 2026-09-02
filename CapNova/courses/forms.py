from django import forms

from .models import Feedback, LearningResource


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
