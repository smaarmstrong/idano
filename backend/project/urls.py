from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

# Create a router and register the ProjectViewSet with it
router = DefaultRouter()
router.register(r"projects", ProjectViewSet)

urlpatterns = [
    # The router automatically handles the create, read, update, and delete actions
    path("api/", include(router.urls)),
]
