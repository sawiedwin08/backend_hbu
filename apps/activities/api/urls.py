from django.urls import path
from apps.activities.api.views.general_views import DimensionListAPIView, ProgramDimensionListAPIView, SubprogramDimensionListAPIView
from .views.attandance_views import QRCodeApiView, RegisterAttandenceApiView, AttandenceListAPIView, AttandenceListByActivityAPIView

urlpatterns = [
    path('dimension/', DimensionListAPIView.as_view(), name='dimension'),
    path('program_dimension/', ProgramDimensionListAPIView.as_view(), name='program_dimension'),
    path('subprogram_dimension/', SubprogramDimensionListAPIView.as_view(), name='subprogram_dimension'),
    path('qr_code/<int:activity_id>/qr_code/', QRCodeApiView.as_view(), name='qr_code'),
    path('register_attandence/', RegisterAttandenceApiView.as_view(), name='register_attandence'),
    path('attandence_student/', AttandenceListAPIView.as_view(), name='attandence_student'),
    path('attandence_activity/<int:activity_id>/', AttandenceListByActivityAPIView.as_view(), name='attandence_activity')
]