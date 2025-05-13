from rest_framework import serializers
import datetime
from apps.activities.models import Activity, Dimension, ProgramDimension, SubprogramDimension
from apps.users.models import UsuarioBienestar
from apps.activities.api.serializers.general_serializers import DimensionSerializer, ProgramDimensionSerializer, SubprogramDimensionSerializer
from apps.users.api.serializers import UsuarioBienestarSerializer

class ActivitySerializer(serializers.ModelSerializer):
    responsible = UsuarioBienestarSerializer()
    class Meta:
        model = Activity
        exclude = ('created_date','modified_date','deleted_date',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'state': instance.state,
            'name': instance.name,
            'description': instance.description,
            'dimension': instance.dimension.name,
            'program_dimension': instance.program_dimension.name,
            'subprogram_dimension': instance.subprogram_dimension.name,
            'responsible': UsuarioBienestarSerializer(instance.responsible).data,
            'date': instance.date,
            'start_hour': instance.start_hour,
            'end_hour': instance.end_hour,
            'count_hours': instance.count_hours,
            'qr_code_identifier': str(instance.qr_code_identifier),
        }
    
    name = serializers.CharField(
        error_messages={
            'required': 'El titulo es obligatorio.',
            'blank': 'El nombre no puede estar vacío.'
        }
    )
    description = serializers.CharField(
        error_messages={
            'required': 'La descripción es obligatoria.',
            'blank': 'La descripción no puede estar vacía.'
        }
    )
    date = serializers.DateField(
        error_messages={
            'required': 'La fecha es obligatoria.',
            'invalid': 'La fecha no tiene un formato válido.'
        }
    )
    start_hour = serializers.TimeField(
        error_messages={
            'required': 'La hora de inicio es obligatoria.',
            'invalid': 'La hora de inicio no tiene un formato válido.'
        }
    )
    end_hour = serializers.TimeField(
        error_messages={
            'required': 'La hora de fin es obligatoria.',
            'invalid': 'La hora de fin no tiene un formato válido.'
        }
    )
    count_hours = serializers.IntegerField(
        error_messages={
            'required': 'La cantidad de horas es obligatoria.',
            'invalid': 'La cantidad de horas debe ser un número entero.'
        }
    )
    dimension = serializers.PrimaryKeyRelatedField(
        queryset=Dimension.objects.all(),
        error_messages={
            'required': 'La dimensión es obligatoria.',
            'does_not_exist': 'La dimensión especificada no existe.'
        }
    )
    
    def validate(self, data):
        required_fields = [
            'name', 'description', 'date', 'start_hour', 
            'end_hour', 'count_hours', 'dimension', 
            'program_dimension', 'subprogram_dimension', 'responsible'
        ]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            errors = {field: ['Este campo es obligatorio.'] for field in missing_fields}
            raise serializers.ValidationError(errors)

        date = data.get('date')
        if date and date < datetime.date.today():
            raise serializers.ValidationError({
                'date': 'La fecha no puede ser anterior a la fecha actual.'
            })

        # Validaciones cruzadas adicionales
        start_hour = data.get('start_hour')
        end_hour = data.get('end_hour')
        if start_hour and end_hour and end_hour <= start_hour:
            raise serializers.ValidationError({
                'start_hour': 'La hora de inicio debe ser menor que la hora de fin.',
                'end_hour': 'La hora de fin debe ser mayor que la hora de inicio.'
            })

        # Calcular la duración y ajustar count_hours
        start_hour_dt = datetime.datetime.strptime(str(start_hour), '%H:%M:%S')
        end_hour_dt = datetime.datetime.strptime(str(end_hour), '%H:%M:%S')
        duration = (end_hour_dt - start_hour_dt).total_seconds() / 3600
        if duration - int(duration) >= 0.5:
            data['count_hours'] = int(duration) + 1
        else:
            data['count_hours'] = int(duration)
        
        return data
    
class EditActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ('created_date','modified_date','deleted_date',)
    
    name = serializers.CharField(
        error_messages={
            'required': 'El titulo es obligatorio.',
            'blank': 'El nombre no puede estar vacío.'
        }
    )
    description = serializers.CharField(
        error_messages={
            'required': 'La descripción es obligatoria.',
            'blank': 'La descripción no puede estar vacía.'
        }
    )
    date = serializers.DateField(
        error_messages={
            'required': 'La fecha es obligatoria.',
            'invalid': 'La fecha no tiene un formato válido.'
        }
    )
    start_hour = serializers.TimeField(
        error_messages={
            'required': 'La hora de inicio es obligatoria.',
            'invalid': 'La hora de inicio no tiene un formato válido.'
        }
    )
    end_hour = serializers.TimeField(
        error_messages={
            'required': 'La hora de fin es obligatoria.',
            'invalid': 'La hora de fin no tiene un formato válido.'
        }
    )
    count_hours = serializers.IntegerField(
        error_messages={
            'required': 'La cantidad de horas es obligatoria.',
            'invalid': 'La cantidad de horas debe ser un número entero.'
        }
    )
    dimension = serializers.PrimaryKeyRelatedField(
        queryset=Dimension.objects.all(),
        error_messages={
            'required': 'La dimensión es obligatoria.',
            'does_not_exist': 'La dimensión especificada no existe.'
        }
    )
    
    def validate(self, data):
        required_fields = [
            'name', 'description', 'date', 'start_hour', 
            'end_hour', 'count_hours', 'dimension', 
            'program_dimension', 'subprogram_dimension', 'responsible'
        ]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            errors = {field: ['Este campo es obligatorio.'] for field in missing_fields}
            raise serializers.ValidationError(errors)

        date = data.get('date')
        if date and date < datetime.date.today():
            raise serializers.ValidationError({
                'date': 'La fecha no puede ser anterior a la fecha actual.'
            })

        # Validaciones cruzadas adicionales
        start_hour = data.get('start_hour')
        end_hour = data.get('end_hour')
        if start_hour and end_hour and end_hour <= start_hour:
            raise serializers.ValidationError({
                'start_hour': 'La hora de inicio debe ser menor que la hora de fin.',
                'end_hour': 'La hora de fin debe ser mayor que la hora de inicio.'
            })

        # Calcular la duración y ajustar count_hours
        start_hour_dt = datetime.datetime.strptime(str(start_hour), '%H:%M:%S')
        end_hour_dt = datetime.datetime.strptime(str(end_hour), '%H:%M:%S')
        duration = (end_hour_dt - start_hour_dt).total_seconds() / 3600
        if duration - int(duration) >= 0.5:
            data['count_hours'] = int(duration) + 1
        else:
            data['count_hours'] = int(duration)
        
        return data