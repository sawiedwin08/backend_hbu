from  rest_framework import generics
from datetime import datetime
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from apps.base.api import GeneralListApiView
from apps.users.authentication_mixins import Authentication

from apps.users.permissions import IsAdmin, IsCollaborator, IsStudent
from apps.activities.api.serializers.activity_serializers import ActivitySerializer, EditActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):

    serializer_class = ActivitySerializer
    print(serializer_class)

    # def get_permissions(self):
        # Define permisos según la acción (action)
        # if self.action in ['list']:
            # permission_classes = [IsAuthenticated]  # Solo autenticados pueden listar
        # else:
            # permission_classes = [IsAuthenticated, IsAdmin]  # Solo admin para otras acciones
            # permission_classes = [IsAuthenticated]  # Solo admin para otras acciones
        # return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def list(self, request):
        activity_serializer = self.get_serializer(self.get_queryset(), many=True)
        # print(activity_serializer.data)
        return Response(activity_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EditActivitySerializer(data=request.data)
        request.data['count_hours'] = 0
        # start_hour = datetime.strptime(request.data['start_hour'], '%H:%M')
        # end_hour = datetime.strptime(request.data['end_hour'], '%H:%M')
        # # calcular la resta de las horas que de resultado en entero aproximado hacia arriba
        # duration = (end_hour - start_hour).total_seconds() / 3600
        # if duration - int(duration) >= 0.5:
        #     request.data['count_hours'] = int(duration) + 1
        # else:
        #     request.data['count_hours'] = int(duration)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Actividad creada correctamente'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            activity_serializer = EditActivitySerializer(self.get_queryset(pk), data=request.data)
            # print(request.data)
            if activity_serializer.is_valid():
                # print('entro')
                activity_serializer.save()
                return Response(activity_serializer.data, status=status.HTTP_200_OK)
            return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity.state = False
            activity.save()
            return Response({'message': 'Actividad eliminada correctamente'}, status=status.HTTP_200_OK)
        return Response({'message': 'Actividad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)