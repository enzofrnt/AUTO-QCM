from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class TeacherRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.groups.filter(name="Enseignant").exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class StudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.groups.filter(name="Etudiant").exists():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class SelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        user_id = kwargs.get("pk")
        if request.user.id != user_id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TeacherOrSelfStudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        user_id = kwargs.get("pk")
        if (
            request.user.groups.filter(name="Enseignant").exists()
            or request.user.id == user_id
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
