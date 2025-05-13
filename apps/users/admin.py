from django.contrib import admin
from apps.users.models import User, Estudiante, UsuarioBienestar, AcademicProgram, Gender, DocumentType

admin.site.register(User)
admin.site.register(Estudiante)
admin.site.register(UsuarioBienestar)
admin.site.register(AcademicProgram)
admin.site.register(Gender)
admin.site.register(DocumentType)
