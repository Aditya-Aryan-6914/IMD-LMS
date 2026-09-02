from django import forms

from .models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["course", "title", "deadline"]
        widgets = {"deadline": forms.DateTimeInput(attrs={"type": "datetime-local"})}

    def __init__(self, *args, trainer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if trainer is not None:
            self.fields["course"].queryset = self.fields["course"].queryset.filter(trainer=trainer)


class QuestionForm(forms.Form):
    """One MCQ question, entered with up to 4 choices in a single form --
    matches the flat, no-JS-framework style already used across this app
    (see LearningResourceForm) rather than a nested formset."""

    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), label="Question text")
    choice_1 = forms.CharField(max_length=300, label="Choice 1")
    choice_2 = forms.CharField(max_length=300, label="Choice 2")
    choice_3 = forms.CharField(max_length=300, required=False, label="Choice 3 (optional)")
    choice_4 = forms.CharField(max_length=300, required=False, label="Choice 4 (optional)")
    correct_choice = forms.ChoiceField(
        choices=[("1", "Choice 1"), ("2", "Choice 2"), ("3", "Choice 3"), ("4", "Choice 4")],
        widget=forms.RadioSelect,
        label="Correct answer",
    )

    def clean(self):
        cleaned = super().clean()
        correct = cleaned.get("correct_choice")
        if correct and not cleaned.get(f"choice_{correct}"):
            self.add_error("correct_choice", "The choice marked correct needs text filled in.")
        return cleaned
