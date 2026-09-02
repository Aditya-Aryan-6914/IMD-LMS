"""
URL configuration for CapNova project.
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('announcements.urls')),   # '' -> public homepage
    path('', include('accounts.urls')),         # register/, login/, dashboard/...
    path('', include('courses.urls')),          # courses/, trainer/library/, competency-map/
    path('', include('assessments.urls')),      # assessments/, trainer/assessments/

    # Password reset flow (linked from login.html). Only these 4 views are
    # wired up -- login/logout/password_change are handled by our own
    # accounts views, so django.contrib.auth.urls is NOT included wholesale
    # to avoid a name collision on 'login'.
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html',
            subject_template_name='auth/password_reset_subject.txt',
            email_template_name='auth/password_reset_email.html',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
