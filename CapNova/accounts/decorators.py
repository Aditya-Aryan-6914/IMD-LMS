from functools import wraps

from django.shortcuts import redirect


def role_required(*roles):
    """Restrict a view to users whose .role is in `roles`. Assumes the user
    is already authenticated (stack this under @login_required, or rely on
    the redirect-to-login fallback below)."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.role not in roles:
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
