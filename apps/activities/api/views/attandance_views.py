from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
from rest_framework.exceptions import NotFound, ValidationError
from datetime import datetime

from apps.activities.models import Activity, AttandenceActivity
from apps.users.models import Estudiante
from apps.activities.api.serializers.attandance_serializers import AttendanceSerializer, AttandenceActivitySerializer

class QRCodeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, activity_id):
        # user = request.user
        # if user.is_authenticated:
        #     return Response({"message": "User is authenticated"})
        # else:
        #     return Response({"message": "User is not authenticated"})
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response({"message": "Activity not found"}, status=404)
        
        activity.qr_code_identifier = uuid.uuid4()
        activity.save()
        return Response({"qr_code_identifier": activity.qr_code_identifier}, status=200)
    
class RegisterAttandenceApiView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        serializer = AttendanceSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            qr_code_identifier = request.data.get("qr_code_identifier")
            student = request.user
            print(request.data.get('student'))
            
        # Buscar al estudiante
            student = Estudiante.objects.get(id=request.data.get('student'))
            # print(student.accumulated_hours)
        #      # Buscar la actividad
            activity = Activity.objects.get(qr_code_identifier=qr_code_identifier)
            # print(activity.count_hours)

            student.accumulated_hours += activity.count_hours
            # print(student.accumulated_hours)
            student.save()
        
        #     # Verificar si el estudiante ya asistio a la actividad
            attandence_activity = AttandenceActivity.objects.filter(activity=activity, student=student).first()
            if not attandence_activity:
                attandence_activity = AttandenceActivity(activity=activity, student=student)

            attandence_activity.attendance_date = datetime.now()
            attandence_activity.save()
            return Response({"message": "Asistencia registrada exitosamente"}, status=200)
        
        return Response(serializer.errors, status=400)

class AttandenceListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = AttandenceActivity.objects.all()
        serializer_class = AttendanceSerializer(queryset, many=True)
        return Response(serializer_class.data, status=200)
    
# listar los estudiantes que asistieron a cierta actividad
class AttandenceListByActivityAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        attandence_activity = AttandenceActivity.objects.filter(activity=activity)
        serializer = AttandenceActivitySerializer(attandence_activity, many=True)
        return Response(serializer.data, status=200)
    
