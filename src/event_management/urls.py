from rest_framework.routers import SimpleRouter

from .views import EventViewSet

router = SimpleRouter()
router.register(r"", EventViewSet)

urlpatterns = router.urls + []
