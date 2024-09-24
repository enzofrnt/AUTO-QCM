# app/mixins.py
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class TeacherRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Enseignant").exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class StudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Etudiant").exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class SelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if request.user.id != user_id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TeacherOrStudentOwnDashboardRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if (
            request.user.groups.filter(name="Enseignant").exists()
            or request.user.id == user_id
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
