from rest_framework.routers import DefaultRouter

from .views import ScoreEventViewSet

router = DefaultRouter()
router.register("", ScoreEventViewSet, basename="scoreevents")

urlpatterns = router.urls