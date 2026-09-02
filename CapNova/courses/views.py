from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import TrainerProfile, User
from .forms import FeedbackForm, LearningResourceForm
from .models import Course, Enrollment, LearningResource, Subject


@login_required
@role_required(User.Role.TRAINEE)
def course_list(request):
    enrolled_ids = Enrollment.objects.filter(trainee=request.user).values_list("course_id", flat=True)
    courses = Course.objects.filter(is_published=True).exclude(id__in=enrolled_ids)
    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
@role_required(User.Role.TRAINEE)
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    enrollment = Enrollment.objects.filter(course=course, trainee=request.user).first()
    resources = course.resources.all() if enrollment else []

    feedback_form = None
    existing_feedback = None
    if enrollment:
        existing_feedback = course.feedback_entries.filter(trainee=request.user).first()
        if not existing_feedback:
            feedback_form = FeedbackForm()
            if request.method == "POST":
                feedback_form = FeedbackForm(request.POST)
                if feedback_form.is_valid():
                    feedback = feedback_form.save(commit=False)
                    feedback.course = course
                    feedback.trainee = request.user
                    feedback.save()
                    messages.success(request, "Thanks for your feedback.")
                    return redirect("course_detail", course_id=course.id)

    context = {
        "course": course,
        "enrollment": enrollment,
        "resources": resources,
        "feedback_form": feedback_form,
        "existing_feedback": existing_feedback,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
@role_required(User.Role.TRAINEE)
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    if request.method == "POST":
        Enrollment.objects.get_or_create(course=course, trainee=request.user)
        messages.success(request, f"Enrolled in {course.title}.")
    return redirect("course_detail", course_id=course.id)


@login_required
@role_required(User.Role.TRAINER)
def trainer_library(request):
    resources = LearningResource.objects.filter(trainer=request.user).select_related("course")

    if request.method == "POST":
        form = LearningResourceForm(request.POST, request.FILES, trainer=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.trainer = request.user
            resource.save()
            messages.success(request, "Resource uploaded to your library.")
            return redirect("trainer_library")
    else:
        form = LearningResourceForm(trainer=request.user)

    return render(request, "courses/trainer_library.html", {"form": form, "resources": resources})


@login_required
def competency_map(request):
    """Trainer -> subject coverage, for finding a suitable trainer for a
    given subject (PS: 'competency mapping for identifying suitable
    trainers for various subjects')."""
    subjects = Subject.objects.prefetch_related("qualified_trainers__user")
    return render(request, "courses/competency_map.html", {"subjects": subjects})
