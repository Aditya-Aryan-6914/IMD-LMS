from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import User
from courses.models import Enrollment
from .forms import QuestionForm, QuestionnaireForm
from .models import Attempt, AttemptAnswer, Choice, Question, Questionnaire


@login_required
@role_required(User.Role.TRAINEE)
def questionnaire_list(request):
    course_ids = Enrollment.objects.filter(trainee=request.user).values_list("course_id", flat=True)
    attempted_ids = Attempt.objects.filter(trainee=request.user).values_list("questionnaire_id", flat=True)
    questionnaires = Questionnaire.objects.filter(course_id__in=course_ids).exclude(id__in=attempted_ids)
    return render(request, "assessments/questionnaire_list.html", {"questionnaires": questionnaires})


@login_required
@role_required(User.Role.TRAINEE)
def take_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(
        Questionnaire.objects.prefetch_related("questions__choices"), id=questionnaire_id
    )

    if not Enrollment.objects.filter(course=questionnaire.course, trainee=request.user).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect("questionnaire_list")

    if questionnaire.is_past_deadline:
        messages.error(request, "The deadline for this assessment has passed.")
        return redirect("questionnaire_list")

    if Attempt.objects.filter(questionnaire=questionnaire, trainee=request.user).exists():
        messages.info(request, "You have already attempted this assessment.")
        return redirect("questionnaire_list")

    questions = questionnaire.questions.all()

    if request.method == "POST":
        attempt = Attempt.objects.create(
            questionnaire=questionnaire, trainee=request.user, total=questions.count()
        )
        score = 0
        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            choice = question.choices.filter(id=choice_id).first() if choice_id else None
            AttemptAnswer.objects.create(attempt=attempt, question=question, selected_choice=choice)
            if choice and choice.is_correct:
                score += 1
        attempt.score = score
        attempt.submitted_at = timezone.now()
        attempt.save(update_fields=["score", "submitted_at"])
        return redirect("questionnaire_result", attempt_id=attempt.id)

    return render(
        request, "assessments/take_questionnaire.html",
        {"questionnaire": questionnaire, "questions": questions},
    )


@login_required
@role_required(User.Role.TRAINEE)
def questionnaire_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, trainee=request.user)
    return render(request, "assessments/questionnaire_result.html", {"attempt": attempt})


@login_required
@role_required(User.Role.TRAINER)
def trainer_questionnaires(request):
    """PS: trainer 'monitors trainee participation and performance'."""
    questionnaires = Questionnaire.objects.filter(trainer=request.user).prefetch_related(
        "attempts__trainee", "questions"
    )
    return render(request, "assessments/trainer_questionnaires.html", {"questionnaires": questionnaires})


@login_required
@role_required(User.Role.TRAINER)
def create_questionnaire(request):
    if request.method == "POST":
        form = QuestionnaireForm(request.POST, trainer=request.user)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.trainer = request.user
            questionnaire.save()
            messages.success(request, "Questionnaire created. Now add questions to it.")
            return redirect("manage_questionnaire", questionnaire_id=questionnaire.id)
    else:
        form = QuestionnaireForm(trainer=request.user)
    return render(request, "assessments/questionnaire_form.html", {"form": form})


@login_required
@role_required(User.Role.TRAINER)
def manage_questionnaire(request, questionnaire_id):
    """Add MCQ questions (with 2-4 choices each) to a questionnaire the
    trainer owns. One question is added per POST, so the trainer can build
    up the question bank incrementally and see what's there so far."""
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, trainer=request.user)
    questions = questionnaire.questions.prefetch_related("choices")

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                questionnaire=questionnaire,
                text=form.cleaned_data["text"],
                order=questions.count(),
            )
            for i in range(1, 5):
                text = form.cleaned_data.get(f"choice_{i}")
                if text:
                    Choice.objects.create(
                        question=question,
                        text=text,
                        is_correct=(str(i) == form.cleaned_data["correct_choice"]),
                    )
            messages.success(request, "Question added.")
            return redirect("manage_questionnaire", questionnaire_id=questionnaire.id)
    else:
        form = QuestionForm()

    return render(
        request, "assessments/manage_questionnaire.html",
        {"questionnaire": questionnaire, "questions": questions, "form": form},
    )


@login_required
@role_required(User.Role.TRAINER)
def delete_question(request, questionnaire_id, question_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, trainer=request.user)
    if request.method == "POST":
        questionnaire.questions.filter(id=question_id).delete()
        messages.info(request, "Question removed.")
    return redirect("manage_questionnaire", questionnaire_id=questionnaire.id)
