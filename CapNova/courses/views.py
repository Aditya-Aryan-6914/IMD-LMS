import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import TrainerProfile, User
from .certificates import generate_certificate_pdf
from .forms import CourseForm, FeedbackForm, LearningResourceForm, SubjectForm
from .models import Certificate, Course, Enrollment, LearningResource, Subject


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


# ---------------------------------------------------------------------------
# Admin: course & subject creation UI (previously only available via
# /admin/ -- see handover doc, "next steps" #1).
# ---------------------------------------------------------------------------

@login_required
@role_required(User.Role.ADMIN)
def admin_course_list(request):
    courses = Course.objects.select_related("subject", "trainer").all()
    return render(request, "courses/admin_course_list.html", {"courses": courses})


@login_required
@role_required(User.Role.ADMIN)
def admin_course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.title}" created.')
            return redirect("admin_course_list")
    else:
        form = CourseForm()
    return render(
        request, "courses/admin_course_form.html",
        {"form": form, "editing": False},
    )


@login_required
@role_required(User.Role.ADMIN)
def admin_course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.title}" updated.')
            return redirect("admin_course_list")
    else:
        form = CourseForm(instance=course)
    return render(
        request, "courses/admin_course_form.html",
        {"form": form, "editing": True, "course": course},
    )


@login_required
@role_required(User.Role.ADMIN)
def admin_course_toggle_publish(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.is_published = not course.is_published
        course.save(update_fields=["is_published"])
        messages.success(
            request,
            f'"{course.title}" is now {"published" if course.is_published else "a draft"}.',
        )
    return redirect("admin_course_list")


@login_required
@role_required(User.Role.ADMIN)
def admin_course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        title = course.title
        course.delete()
        messages.info(request, f'Course "{title}" deleted.')
    return redirect("admin_course_list")


@login_required
@role_required(User.Role.ADMIN)
def admin_subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject "{subject.name}" added.')
            return redirect("admin_course_create")
    else:
        form = SubjectForm()
    return render(request, "courses/admin_subject_form.html", {"form": form})


# ---------------------------------------------------------------------------
# Certificates (next-steps item #2 from handover.md): trainer marks an
# enrollment complete -> a Certificate row is generated -> trainee can
# download a PDF -> anyone can verify a certificate number publicly.
# ---------------------------------------------------------------------------

def _generate_certificate_number(course, enrollment):
    return f"IMD-{course.id:04d}-{enrollment.id:04d}-{secrets.token_hex(3).upper()}"


@login_required
@role_required(User.Role.TRAINER)
def trainer_course_enrollments(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    enrollments = course.enrollments.select_related("trainee", "certificate").order_by("-enrolled_at")
    return render(
        request, "courses/trainer_course_enrollments.html",
        {"course": course, "enrollments": enrollments},
    )


@login_required
@role_required(User.Role.TRAINER)
def mark_enrollment_complete(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__trainer=request.user)
    if request.method == "POST":
        if enrollment.status != Enrollment.Status.COMPLETED:
            enrollment.status = Enrollment.Status.COMPLETED
            enrollment.completed_at = timezone.now()
            enrollment.save(update_fields=["status", "completed_at"])

        certificate = getattr(enrollment, "certificate", None)
        if certificate is None:
            certificate = Certificate.objects.create(
                enrollment=enrollment,
                certificate_number=_generate_certificate_number(enrollment.course, enrollment),
            )
        messages.success(
            request,
            f"{enrollment.trainee.full_name} marked complete. Certificate {certificate.certificate_number} issued.",
        )
    return redirect("trainer_course_enrollments", course_id=enrollment.course_id)


@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    enrollment = certificate.enrollment
    is_owner = request.user == enrollment.trainee
    is_course_trainer = request.user == enrollment.course.trainer
    is_admin = request.user.role == User.Role.ADMIN
    if not (is_owner or is_course_trainer or is_admin):
        messages.error(request, "You don't have access to that certificate.")
        return redirect("dashboard")

    pdf_bytes = generate_certificate_pdf(certificate)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{certificate.certificate_number}.pdf"'
    return response


def verify_certificate(request, certificate_number):
    """Public verification page -- no login required, matches how
    printed/shared certificates get checked."""
    certificate = Certificate.objects.select_related(
        "enrollment__trainee", "enrollment__course__subject"
    ).filter(certificate_number=certificate_number).first()
    return render(
        request, "courses/certificate_verify.html",
        {"certificate": certificate, "certificate_number": certificate_number},
    )
