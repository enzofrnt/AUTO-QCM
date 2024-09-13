# app/mixins.py
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

class TeacherRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_type != 'Enseignant':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_type != 'Etudiant':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class SelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if request.user.id != user_id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class TeacherOrStudentOwnDashboardRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if request.user.profile.user_type == 'Enseignant' or request.user.id == user_id:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
