from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

class TeacherRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            # Redirige vers la page de login (géré par LoginRequiredMixin)
            return self.handle_no_permission()

        # Vérifier le type d'utilisateur
        if request.user.utilisateur.user_type != 'Enseignant':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.utilisateur.user_type != 'Etudiant':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class SelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_id = kwargs.get('pk')
        if request.user.id != user_id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class TeacherOrSelfStudentRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_id = kwargs.get('pk')
        if request.user.utilisateur.user_type == 'Enseignant' or request.user.id == user_id:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
