from rest_framework import serializers
from apps.activities.models import AttandenceActivity, Activity
from apps.users.models import Estudiante
from apps.users.api.serializers import EstudianteSerializer
from rest_framework.exceptions import ValidationError

class AttendanceSerializer(serializers.ModelSerializer):
    qr_code_identifier = serializers.UUIDField(required=True)

    class Meta:
        model = AttandenceActivity
        fields = '__all__'

    def validate_qr_code_identifier(self, value):
        try:
            # Verificar si el QR corresponde a una actividad válida
            activity = Activity.objects.get(qr_code_identifier=value)
        except Activity.DoesNotExist:
            raise ValidationError("Código QR inválido o caducado")
        return value

    def validate(self, data):
        qr_code_identifier = data['qr_code_identifier']
        student = self.context['request'].user  # Obtener el estudiante actual

        # Verificar si el estudiante ya está registrado en la actividad
        try:
            activity = Activity.objects.get(qr_code_identifier=qr_code_identifier)
            attendance_entry = AttandenceActivity.objects.filter(activity=activity, student=student).first()

            if attendance_entry and attendance_entry.attendance_date:
                raise ValidationError("Ya has registrado asistencia para esta actividad")

        except Activity.DoesNotExist:
            raise ValidationError("Código QR inválido o caducado")

        return data

class AttandenceActivitySerializer(serializers.ModelSerializer):
    student = EstudianteSerializer()
    class Meta:
        model = AttandenceActivity
        fields = '__all__'