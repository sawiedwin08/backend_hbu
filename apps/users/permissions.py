from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.is_authenticated and request.user.role == 'Administrador'

class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Usuario_Bienestar'
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Estudiante'