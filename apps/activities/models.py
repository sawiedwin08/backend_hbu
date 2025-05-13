from django.db import models
from simple_history.models import HistoricalRecords
import uuid

from apps.base.models import BaseModel
from apps.users.models import UsuarioBienestar, Estudiante

class Dimension(BaseModel):
    name = models.CharField('Nombre Dimension', max_length=255)
    description = models.TextField('Descripcion', max_length=255)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Dimension'
        verbose_name_plural = 'Dimensiones'

    def __str__(self):
        return f'{self.name}'
    
class ProgramDimension(BaseModel):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    name = models.CharField('Nombre Programa', max_length=255)
    description = models.TextField('Descripcion', max_length=255)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Programa Dimension'
        verbose_name_plural = 'Programas Dimension'

    def __str__(self):
        return f'{self.name}'
    
class SubprogramDimension(BaseModel):
    program_dimension = models.ForeignKey(ProgramDimension, on_delete=models.CASCADE)
    name = models.CharField('Nombre Subprograma', max_length=255)
    description = models.TextField('Descripcion', max_length=255)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Subprograma Dimension'
        verbose_name_plural = 'Subprogramas Dimension'

    def __str__(self):
        return f'{self.name}'
    
class Activity(BaseModel):
    name = models.CharField('Nombre Actividad', max_length=255)
    description = models.TextField('Descripcion', max_length=255)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    program_dimension = models.ForeignKey(ProgramDimension, on_delete=models.CASCADE)
    subprogram_dimension = models.ForeignKey(SubprogramDimension, on_delete=models.CASCADE)
    responsible = models.ForeignKey(UsuarioBienestar, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    start_hour = models.TimeField('Hora de inicio')
    end_hour = models.TimeField('Hora de fin')
    count_hours = models.IntegerField('Cantidad de horas')
    qr_code_identifier = models.UUIDField('Identificador QR', default=uuid.uuid4, editable=False, unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return f'Actividad {self.name} pertenece al subprograma {self.subprogram_dimension}'


class AttandenceActivity(BaseModel):
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    student = models.ForeignKey('users.Estudiante', on_delete=models.PROTECT)
    # qr_code_identifier = models.UUIDField('Identificador QR', default=uuid4, editable=False, unique=True)
    attendance_date = models.DateTimeField('Fecha de Asistencia', null=True, blank=True)
    historical = HistoricalRecords()
    class Meta:
        verbose_name = 'Registro de Actividad'
        verbose_name_plural = 'Registros de Actividades'
        unique_together = ('activity', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.activity.name}"
