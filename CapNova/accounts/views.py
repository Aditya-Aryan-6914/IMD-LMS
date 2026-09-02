from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Enrollment, LearningResource, Subject
from .decorators import role_required
from .forms import LoginForm, RegisterForm, TraineeProfileForm, TrainerProfileForm
from .models import TraineeProfile, TrainerProfile, User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    category = request.POST.get("category", "trainer")
    if request.method == "POST":
        form = RegisterForm(request.POST, category=category)
        if form.is_valid():
            user = form.save()
            if user.is_approved:
                messages.success(request, "Account created successfully. You can now log in.")
            else:
                messages.info(
                    request,
                    "Account created. It is pending admin approval before you can log in.",
                )
            return redirect("login")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm(category=category)

    return render(request, "auth/register.html", {"form": form, "category": category})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is None:
                messages.error(request, "Invalid email or password.")
            elif not user.is_active:
                messages.error(request, "This account has been deactivated.")
            elif not user.is_approved:
                messages.error(request, "Your account is pending admin approval.")
            else:
                auth_login(request, user)
                return redirect("dashboard")
        else:
            messages.error(request, "Please enter a valid email and password.")

    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard_router(request):
    """Single entry point ('/dashboard/') that sends each role to its own
    dashboard -- this is the role-based routing the PS asks for."""
    role = request.user.role
    if role == User.Role.TRAINEE:
        return redirect("trainee_dashboard")
    if role == User.Role.TRAINER:
        return redirect("trainer_dashboard")
    if role == User.Role.ADMIN:
        return redirect("admin_dashboard")
    return redirect("login")


@login_required
@role_required(User.Role.TRAINEE)
def trainee_dashboard(request):
    profile, _ = TraineeProfile.objects.get_or_create(user=request.user)
    enrollments = Enrollment.objects.filter(trainee=request.user).select_related("course", "certificate")
    enrolled_ids = enrollments.values_list("course_id", flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_ids).filter(is_published=True)[:6]

    context = {
        "profile": profile,
        "enrollments": enrollments,
        "available_courses": available_courses,
    }
    return render(request, "dashboard/trainee_dashboard.html", context)


@login_required
@role_required(User.Role.TRAINEE)
def trainee_profile_edit(request):
    profile, _ = TraineeProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = TraineeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("trainee_dashboard")
    else:
        form = TraineeProfileForm(instance=profile)
    return render(request, "dashboard/trainee_profile_edit.html", {"form": form})


@login_required
@role_required(User.Role.TRAINER)
def trainer_dashboard(request):
    profile, _ = TrainerProfile.objects.get_or_create(user=request.user)
    courses = Course.objects.filter(trainer=request.user)
    resources = LearningResource.objects.filter(trainer=request.user).order_by("-uploaded_at")[:8]
    total_trainees = Enrollment.objects.filter(course__trainer=request.user).values("trainee").distinct().count()

    context = {
        "profile": profile,
        "courses": courses,
        "resources": resources,
        "total_trainees": total_trainees,
    }
    return render(request, "dashboard/trainer_dashboard.html", context)


@login_required
@role_required(User.Role.TRAINER)
def trainer_profile_edit(request):
    profile, _ = TrainerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = TrainerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("trainer_dashboard")
    else:
        form = TrainerProfileForm(instance=profile)
    return render(request, "dashboard/trainer_profile_edit.html", {"form": form})


@login_required
@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    context = {
        "pending_users": User.objects.filter(is_approved=False),
        "total_trainees": User.objects.filter(role=User.Role.TRAINEE).count(),
        "total_trainers": User.objects.filter(role=User.Role.TRAINER).count(),
        "total_courses": Course.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
        "total_subjects": Subject.objects.count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
@role_required(User.Role.ADMIN)
def approve_user(request, user_id):
    if request.method == "POST":
        target = get_object_or_404(User, id=user_id)
        target.is_approved = True
        target.save(update_fields=["is_approved"])
        messages.success(request, f"{target.full_name} approved.")
    return redirect("admin_dashboard")


@login_required
@role_required(User.Role.ADMIN)
def reject_user(request, user_id):
    if request.method == "POST":
        target = get_object_or_404(User, id=user_id)
        target.delete()
        messages.info(request, "Registration rejected and removed.")
    return redirect("admin_dashboard")
