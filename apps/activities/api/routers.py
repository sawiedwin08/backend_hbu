from rest_framework.routers import DefaultRouter
from apps.activities.api.views.activity_viewsets import ActivityViewSet

router = DefaultRouter()

router.register(r'activities', ActivityViewSet, basename = 'activities')

urlpatterns = router.urls
