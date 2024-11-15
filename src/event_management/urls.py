from rest_framework.routers import SimpleRouter

from .views import EventViewSet, ReservationViewSet

router = SimpleRouter()
router.register(r"event", EventViewSet)
router.register(r"reservation", ReservationViewSet, basename="reservation")

urlpatterns = router.urls + []
