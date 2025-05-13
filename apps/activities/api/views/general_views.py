from apps.base.api import GeneralListApiView
from apps.activities.api.serializers.general_serializers import DimensionSerializer, ProgramDimensionSerializer, SubprogramDimensionSerializer
from apps.activities.models import Dimension

from rest_framework.response import Response
from rest_framework import status


class DimensionListAPIView(GeneralListApiView):
    serializer_class = DimensionSerializer

class ProgramDimensionListAPIView(GeneralListApiView):
    serializer_class = ProgramDimensionSerializer

class SubprogramDimensionListAPIView(GeneralListApiView):
    serializer_class = SubprogramDimensionSerializer
