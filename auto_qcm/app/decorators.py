from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def self_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_id = kwargs.get('pk')  # Obtenir l'ID de l'utilisateur depuis les kwargs
        if request.user.id == user_id:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def teacher_or_student_own_dashboard_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_id = kwargs.get('pk')  # Obtenir l'ID de l'utilisateur depuis les kwargs
        if request.user.utilisateur.user_type == 'Enseignant' or request.user.id == user_id:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.utilisateur.user_type == 'Enseignant':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view