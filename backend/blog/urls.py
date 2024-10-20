from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet

# Create a router and register the BlogPostViewSet with it
router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet)

urlpatterns = [
    # The router automatically handles the create, read, update, and delete actions
    path('', include(router.urls)),  # This will handle the API endpoints
]
