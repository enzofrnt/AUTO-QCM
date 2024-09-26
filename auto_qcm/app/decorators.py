from django.core.exceptions import PermissionDenied


def self_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_id = kwargs.get("pk")  # Obtenir l'ID de l'utilisateur depuis les kwargs
        if request.user.id == user_id:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return _wrapped_view


def teacher_or_self_student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_id = kwargs.get("pk")  # Obtenir l'ID de l'utilisateur depuis les kwargs
        if (
            request.user.groups.filter(name="Enseignant").exists()
            or request.user.id == user_id
        ):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return _wrapped_view


def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name="Enseignant").exists():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return _wrapped_view
